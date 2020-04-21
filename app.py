
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource, marshal_with
from flask_cors import CORS
import datetime
from stocklab.db_handler.mongodb_handler import MongoDBHandler
from app_field import AppField

app = Flask(__name__)
CORS(app)
api = Api(app)

mongo = MongoDBHandler()

class CodeList(Resource):
    """
    @marshal_with(AppField.code_list_fields)
    def get(self):
        market = request.args.get('market', default="0", type=str)
        if market == "0":
            results = list(mongo.find_item({}, "stocklab", "code_info"))
        elif market == "1" or market == "2":
            result = list(mongo.find_item({"시장구분":market}, "stocklab", "code_info"))
        result_list = []
        for item in results:
            code_info = {}
            code_info = { AppField.code_hname_to_eng[field]: item[field] for field in item.keys() if field in AppField.code_hname_to_eng}
            result_list.append(code_info)
        return {"code_list": result_list, "count": len(result_list)}, 200
    """
    def get(self):
        results = list(mongo.find_item({}, "stocklab_ace", "code_info"))
        result_list = []
        for item in results:
            code_info = {}
            code_info = {AppField.code_hname_to_eng[field]: item[field] for field in item.keys() if
                         field in AppField.code_hname_to_eng}
            result_list.append(code_info)
        return {"code_list": result_list, "count": len(result_list)}, 200

class Code(Resource):
    """
    @marshal_with(AppField.code_fields)
    def get(self, code):
        result = mongo.find_item_one({"단축코드": code}, "stocklab", "code_info")
        if result is None:
            return {}, 404
        code_info = {}
        code_info = { AppField.code_hname_to_eng[field]: result[field] for field in result.keys() if field in AppField.code_hname_to_eng}
        return code_info
    """
    def get(self, code):
        result = mongo.find_item_one({"code": code}, "stocklab_ace", "code_info")
        return result

class Price(Resource):
    def get(self, code):
        pass

class OrderList(Resource):
    def get(self):
        pass

api.add_resource(CodeList, "/codes", endpoint="codes")
api.add_resource(Code, "/codes/<string:code>", endpoint="code")
api.add_resource(Price, "/codes/<string:code>/price", endpoint="price")
api.add_resource(OrderList, "/orders", endpoint="orders")

if __name__ == '__main__':
    app.run(debug=True)
