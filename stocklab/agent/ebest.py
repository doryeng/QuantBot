import configparser
import win32com.client
import pythoncom
from datetime import datetime
import time
from .field import Field

class XASession:
    login_state = 0

    def OnLogin(self, code, msg):
        # 로그인 시도 후 호출되는 이벤트
        # code가 0000이면 로그인 성공
        if code=="0000":
            print(code, msg)
            XASession.login_state = 1
        else:
            print(code, msg)

    def OnDisconnect(self):
        # 서버와의 연결이 끊어지면 발생하는 이벤트
        print("Session disconnected")
        XA_Session.login_state = 0

class EBest:

    QUERY_LIMIT_10MIN = 200
    LIMIT_SECONDS = 600 #10minute

    def __init__(self, mode=None):
        # config.ini 파일을 로드해 사용자ㅡ 서버 정보 저장
        # query_cnt는 10분당 200개의 TR 수행을 관리하기 위한 리스트
        # xa_session_client는 XASession 객체
        # :param mode:str - 모의서버는 demo, 실서버는 prod로 구분
        if mode not in ["PROD","DEMO"]:
            raise Exception("Need to run_mode(PROD or DEMO)")

        run_mode = "EBEST_"+mode
        config = configparser.ConfigParser()
        config.read('C:\\Users\\mskwon\\Documents\\GitHub\\QuantBot\\conf\\config.ini')
        self.user = config[run_mode]['user']
        self.passwd = config[run_mode]['password']
        self.cert_passwd = config[run_mode]['cert_passwd']
        self.host = config[run_mode]['host']
        self.port = config[run_mode]['port']
        self.account = config[run_mode]['account']

        self.xa_session_client = win32com.client.DispatchWithEvents("XA_Session.XASession",XASession)
        self.query_cnt = []

    def _execute_query(self, res, in_block_name, out_block_name, *out_fields, **set_fields):
        # TR코드를 실행하기 위한 메서드입니다.
        # :param res:str 리소스 이름(TR)
        # :param in_block_name:str 인 블록 이름
        # :param out_block_name:str 아웃 블록 이름
        # :param out_params:list 출력 필드 리스트
        # :param in_params:dick 인 블록에 설정할 필드 딕셔너리
        # :param result: list 결과를 list에 담아 반환
        time.sleep(1)
        print("current query cnt:", len(self.query_cnt))
        print(res, in_block_name, out_block_name)
        while len(self.query_cnt) >= EBest.QUERY_LIMIT_10MIN:
            time.sleep(1)
            print("waiting for execute query... current query cnt:", len(self.query_cnt))
            self.query_cnt = list(filter(lambda x: (datetime.today() - x).total_seconds() < EBest.LIMIT_SECONDS, self.query_cnt))

        xa_query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQuery)
        xa_query.LoadFromResFile(XAQuery.RES_PATH+res+".res")
        #in_block_name 셋팅
        for key, value in set_fields.items():
            xa_query.SetFieldData(in_block_name, key, 0 ,value)
        errorCode = xa_query.Request(0)

        #요청 후 대기
        waiting_cnt = 0
        while xa_query.tr_run_state == 0:
            waiting_cnt +=1
            if(waiting_cnt%100000==0):
                print("Waiting....", self.xa_session_client.GetLastError())
            pythoncom.PumpWaitingMessages()

        #결과 블록
        result = []
        count = xa_query.GetBlockCount(out_block_name)

        for i in range(count):
            item = {}
            for field in out_fields:
                value = xa_query.GetFieldData(out_block_name, field, i)
                item[field] = value
            result.append(item)

        #제약시간 체크
        XAQuery.tr_run_state = 0
        self.query_cnt.append(datetime.today())

        #영문 필드명을 한글 필드명으로 변환
        for item in result:
            for field in list(item.keys()):
                if getattr(Field, res, None):
                    res_field = getattr(Field, res, None)
                    if out_block_name in res_field:
                        field_hname = res_field[out_block_name]
                        if field in field_hname:
                            item[field_hname[field]] = item[field]
                            item.pop(field)
        return result

    def get_code_list(self, market=None):
        # TR: t8436 코스피, 코스닥의 종목 리스트를 가져온다.
        # :param market:str 전체(0), 코스피(1), 코스닥(2)
        # :return result:list 시장별 종목 리스트
        if market !="ALL" and market !="KOSPI" and market!="KOSDAQ":
            raise Exception("Need to market param(ALL, KOSPI, kOSDAQ)")

        market_code = {"ALL":"0", "KOSPI":"1", "KOSDAQ":"2"}
        in_params = {"gubun":market_code[market]}
        out_params = ["hname", "shcode", "expcode", "etfgubun", "memedan", "gubun", "spac_gubun"]
        result = self._execute_query("t8436", "t8436InBlock", "t8436OutBlock", *out_params, **in_params)

        return result

    def get_stock_price_by_code(self, code=None, cnt="1"):
        # TR: t1305  현재 날짜를 기준으로 cnt 만큼 전일의 데이터를 가져온다.
        # :param code:str 종목코드
        # :param cnt:str 이전 데이터 조회 범위(일단위)
        # :param result:list 종목의 최근 가격 정보
        in_params = {"shcode":code, "dwmcode":"1", "date":"", "idx":"", "cnt":cnt}
        out_params =['date', 'open', 'high', 'low', 'close', 'sign',
                    'change', 'diff', 'volume', 'diff_vol', 'chdegree',
                    'sojinrate', 'changerate', 'fpvolume', 'covolume',
                    'value', 'ppvolume', 'o_sign', 'o_change', 'o_diff',
                    'h_sign', 'h_change', 'h_diff', 'l_sign', 'l_change',
                    'l_diff', 'marketcap']
        result = self._execute_query("t1305", "t1305InBlock", "t1305OutBlock1", *out_params, **in_params)

        for item in result:
            item["code"] = code
        return result

    def get_account_info(self):
        # TR: CSPAQ12200 현물계좌 예수금/주문가능금액/총평가
        # :return result:list Field CSPAQ12200 참고
        in_params = {"RecCnt":1, "AcntNo": self.account, "Pwd": self.passwd}
        out_params = ["MnyOrdAbleAmt", "BalEvalAmt", "DpsastTotamt", "InvstOrgAmt", "InvstPlAmt", "Dps"]
        result = self._execute_query("CSPAQ12200", "CSPAQ12200InBlock1", "CSPAQ12200OutBlock2", *out_params, **in_params)
        return result

    def get_accout_stock_info(self):
        # TR: CSPAQ12300 현물계좌 잔고내역 조회
        # :return result:list 계좌 보유 종목 정보
        in_params = {"RecCnt":1, "AcntNo": self.account, "Pwd": self.passwd, "BalCreTp": "0",
        "CmsnAppTpCode": "0", "D2balBaseQryTp": "0", "UprcTpCode": "0"}
        out_params = ["IsuNo", "IsuNm", "BalQty", "SellPrc", "BuyPrc", "NowPrc", "AvrUprc", "BalEvalAmt", "PrdayCprc"]
        result = self._execute_query("CSPAQ12300", "CSPAQ12300InBlock1", "CSPAQ12300OutBlock3", *out_params, **in_params)
        return result

    # 테스트 해야함
    def order_stock(self, code, qty, price, bns_type, order_type):
        # TR: CSPAT00600 현물 정상 주문
        # :param btn_type:str 매매타입, 1:매도, 2:매수
        # :param order_type:str 호가유형, 00:지정가, 03: 시장가, 05: 조건부지정가, 07:최우선지정가,
        # 61:장개시전시간외 종가, 81:시간외종가, 82:시간외단일가
        # :return result:dict 주문 관련 정보
        in_params = {"AcntNo": self.account, "InptPwd": self.passwd, "IsuNo": code, "OrdQty": qty,
        "OrdPrc": price, "BnsTpCode": bns_type, "OrdprcPtnCode": order_type, "MgntrnCode": "000", "LoanDt": "", "OrdCndiTpCode":"0"}
        out_params = ["OrdNo", "OrdTime", "OrdMktCode", "OrdPtnCode", "ShtnIsuNo", "MgempNo", "OrdAmt", "SpotOrdQty", "IsuNm"]
        result = self._execute_query("CSPAT00600", "CSPAT00600InBlock1", "CSPAT00600OutBlock2", *out_params, **in_params)
        return result

    # 테스트 해야함
    def order_cancel(self, order_no, code, qty):
        # TR: CSPAT00800 현물 취소 주문
        # :param order_no:str 주문번호
        # :param code:str 종목 코드
        # :param qty:str 취소 수량
        # :return result:dict 취소 결과
        in_params = {"OrgOrdNo": order_no, "AcntNo": self.account, "InptPwd": self.passwd, "IsuNo": code, "OrdQty":qty}
        out_params = ["OrdNo", "PrntOrdNo", "OrdTime", "OrdPtnCode", "IsuNm"]
        result = slef._execute_query("CSPAT00800", "CSPAT00800InBlock1", "CSPAT00800OutBlock2", *out_params, **in_params)
        return result

    # 테스트 해야함
    def order_check(self, order_no):
        # TR: t0425 주식 체결/미체결
        # :param code:str 종목코드
        # :param order_no:str 주문번호
        # :return result:dict 주문번호의 체결상태
        in_params = {"accno": self.account, "passwd": self.passwd, "expcode": code,
        "chegb": "0", "medosu": "0", "sortgb": "1", "cts_ordno": " "}
        out_params =["ordno", "expcode", "medosu", "qty", "price", "cheqty", "cheprice", "ordrem",
        "cfmqty", "status", "orgordno", "ordgb", "ordermtd", "sysprocseq", "hogagb", "price1", "orggb", "singb", "loandt"]
        result_list = self._execute_query("t0425", "t0425InBlock", "t0425OutBlock1", *out_params, **in_params)
        result = {}
        if order_no is not None:
            for item in result_list:
                if item["주문번호"] == order_no:
                    result = item
            return result
        else:
            return result_list

    def get_current_call_price_by_code(self, code=None):
        # TR: t1101 주식 현재가 호가 조회
        # :param code:str 종목코드
        tr_code = "t1101"
        in_params = {"shcode": code}
        out_params = ["hname", "price", "sign", "change", "diff", "volume", "jnilclose",
        "offerho1", "bidho1", "offerrem1", "bidrem1", "offerho2", "bidho2", "offerrem2", "bidrem2",
        "offerho3", "bidho3", "offerrem3", "bidrem3", "offerho4", "bidho4", "offerrem4", "bidrem4",
        "offerho5", "bidho5", "offerrem5", "bidrem5", "offerho6", "bidho6", "offerrem6", "bidrem6",
        "offerho7", "bidho7", "offerrem7", "bidrem7", "offerho8", "bidho8", "offerrem8", "bidrem8",
        "offerho9", "bidho9", "offerrem9", "bidrem9", "offerho10", "bidho10", "offerrem10", "bidrem10",
        "preoffercha10", "prebidcha10", "offer", "bid", "preoffercha", "prebidcha", "hotime", "yeprice", "yevolume",
        "yesign", "yechange", "yediff", "tmoffer", "tmbid", "ho_status", "shcode", "uplmtprice", "dnlmtprice",
        "open", "high", "low"]
        result = self._execute_query("t1101", "t1101InBlock", "t1101OutBlock", *out_params, **in_params)
        for item in result:
            item["code"] = code
        return result

    def get_tick_size(self, price):
        # 호가 단위 조회 메서드
        # :param price:int 가격
        # :return 호가단위
        if price<1000: return 1
        elif price>=1000 and price<5000: return 5
        elif price>=5000 and price<10000: return 10
        elif price>=10000 and price<50000: return 50
        elif price>=50000 and price<100000: return 100
        elif price>=100000 and price<500000: return 500
        elif price>=500000: return 1000

    def login(self):
        self.xa_session_client.ConnectServer(self.host, self.port)
        self.xa_session_client.Login(self.user, self.passwd, self.cert_passwd, 0, 0)
        while XASession.login_state == 0:
            pythoncom.PumpWaitingMessages()

    def logout(self):
        #result = self.xa_session_client.Logout()
        #if result:
        XASession.login_state = 0
        self.xa_session_client.DisconnectServer()

class XAQuery:
    RES_PATH="C:\\eBEST\\xingAPI\\Res\\"
    tr_run_state = 0

    def OnReceiveData(self, code):
        print("OnReceivedData", code)
        XAQuery.tr_run_state = 1

    def OnReceiveMessage(self, error, code, message):
        print("OnreceiveMessage", error, code, message)
