from flask_restful import fields

class AppField:
    code_hname_to_eng = {
        "단축코드": "code",
        "확장코드": "extend_code",
        "종목명": "name",
        "시장구분": "market",
        "ETF구분": "is_etf",
        "주문수량단위": "memedan",
        "기업인수목적회사구분": "is_spac"
    }

    price_hname_to_eng = {
        "날짜": "date",
        "종가": "close",
        "시가": "open",
        "고가": "high",
        "저가": "low",
        "전일대비": "diff",
        "전일대비구분": "diff_type"
    }

    code_fields = {
        "code": fields.String,
        "extend_code": fields.String,
        "name": fields.String,
        "memedan": fields.Integer,
        "market": fields.String,
        "is_etf": fields.String,
        "is_spac": fields.String,
        "uri": fields.Url("code")
    }

    code_list_short_fields = {
        "code": fields.String,
        "name": fields.String
    }
    code_list_fields = {
        "count": fields.Integer,
        "code_list": fields.List(fields.Nested(code_fields)),
        "uri": fields.Url("codes")
    }

    price_fields = {
        "date": fields.Integer,
        "start": fields.Integer,
        "close": fields.Integer,
        "open": fields.Integer,
        "high": fields.Integer,
        "low": fields.Integer,
        "diff": fields.Float,
        "diff_type": fields.Integer
    }

    price_list_fields = {
        "count": fields.Integer,
        "price_list": fields.List(fields.Nested(price_fields)),
    }