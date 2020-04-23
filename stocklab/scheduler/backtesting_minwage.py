from multiprocessing import Process
import time
from datetime import datetime, timedelta
import inspect

from apscheduler.schedulers.background import BackgroundScheduler

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from agent.ebest import EBest
from db_handler.mongodb_handler import MongoDBHandler

ebest_ace = EBest("ACE")
ebest_ace.login()
mongo = MongoDBHandler()

def run_process_trading_scenario(code_list, date):
    p = Process(target=run_trading_scenario, args=(code_list, date))
    p.start()
    p.join()
    print("run porcess join")
    ebest_ace.logout()
    print("EBest LogOut")

def check_buy_completed_order(code):
    # 매수 완료된 주문은 매도 주문
    return 0

def check_buy_order(code):
    # 매수 주문 완료 체크
    return 0

def check_sell_order(code):
    # 매도 주문 완료 체크
    return 0

def run_trading_scenario(code_list, date):
    tick = 0
    #print(code_list, date, tick)

    for code in code_list:
        current_price = ebest_ace.get_price_n_min_by_code(date, code, tick)
        print("current price", current_price)
        # 주식 사기
        order_price = current_price["시가"]
        order = ebest_ace.order_stock(code, "2", order_price, "2", "00")
        order[0]["amount"] = 2
        print("order : ", order)
        mongo.insert_item_one({"매수주문": order, "code": code, "status": "buy_ordered"}, "stocklab_test", "order")

    while tick < 20:
        print("ticK:", tick)
        for code in code_list:
            current_price = ebest_ace.get_price_n_min_by_code(date, code, tick)
            print("current price", current_price)

            # 주식 주문 확인
            buy_order_list = list(mongo.find_item({"$and":[{"code": code}, {"status": "buy_ordered"}]}, "stocklab_test", "order"))
            for buy_order in buy_order_list:
                print("buy_order : ", buy_order)
                order_no = buy_order["매수주문"][0]["주문번호"]
                order_cnt = buy_order["매수주문"][0]["실물주문수량"]
                check_result = ebest_ace.order_check(order_no)
                print("check_result : ", check_result)
                if len(check_result) != 0:
                    result_cnt = check_result["체결수량"]
                    if order_cnt == result_cnt:
                        mongo.update_item({"매수완료.주문번호": order_no}, {"$set": {"매수완료": check_result, "status": "buy_completed"}}, "stocklab_test", "order")
                        # 매수 완료했으니까 또 주식 사기
                        order_price = current_price["시가"]
                        order = ebest_ace.order_stock(code, "2", order_price, "2", "00")
                        order[0]["amount"] = 2
                        print("order : ", order)
                        mongo.insert_item_one({"매수주문": order, "code": code, "status": "buy_ordered"}, "stocklab_test",
                                              "order")

            """
            buy_order_list = ebest_ace.order_stock(code, "2", current_price["시가"], "2", "00")
            buy_order = buy_order_list[0]
            buy_order["amount"] = 2
            mongo.insert_item_one(buy_order, "stocklab_test", "order")
            
            sell_order_list = ebest_ace.order_stock(code, "1", current_price["종가"], "1", "00")
            sell_order = sell_order_list[0]
            sell_order["amount"] = 1
            mongo.insert_item_one(sell_order, "stocklab_test", "order")
            """
        tick += 1
        time.sleep(30)

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    codes = ["180640", "005930"]
    mongo.delete_item_many({},"stocklab_test","order")
    day = datetime.now() - timedelta(days=4)
    day = day.strftime("%Y%m%d")
    print(day)
    scheduler.add_job(func=run_process_trading_scenario, trigger="date", run_date=datetime.now(), id="test",
                    kwargs={"code_list":codes, "date":day})
    scheduler.start()
    """
    while True:
        print("waiting...", datetime.now())
        time.sleep(1)
    """