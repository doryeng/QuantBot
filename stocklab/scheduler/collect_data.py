import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from stocklab.agent.ebest import EBest
from stocklab.db_handler.mongodb_handler import MongoDBHandler

from datetime import datetime
import inspect

"""
def run_process_collect_code_list():
    print(inspect.stack()[0][3])
    p = Process(target=collect_code_list)
    p.start()
    p.join()

def run_process_collect_stock_info():
    print(inspect.stack()[0][3])
    p = Process(target=collect_stock_info)
    p.start()
    p.join()
"""

ebest = EBest("DEMO")
mongodb = MongoDBHandler()
ebest.login()
db_name = "stocklab_ace"

def collect_code_list():
    print(inspect.stack()[0][3])
    result = ebest.get_code_list("ALL")
    mongodb.delete_item_many({}, db_name, "code_info")
    mongodb.insert_item_many(result, db_name, "code_info")
    ebest.logout()

def collect_price_info():
    print(inspect.stack()[0][3])
    code_list = mongodb.find_item({}, db_name, "code_info")
    target_code = set(item["단축코드"] for item in code_list)
    today = datetime.today().strftime("%Y%m%d")
    print(today)

    collect_list = mongodb.find_item({"날짜:":today}, db_name, "price_info").distinct("code")
    for col in collect_list:
        target_code.remove(col)

    for code in target_code:
        print(code)
        result_price = ebest.get_stock_price_by_code(code, "1")
        #print(result_price)
        if len(result_price) > 0:
            print(result_price)
            mongodb.insert_item_many(result_price, db_name, "price_info")

def collect_credit_info():
    print(inspect.stack()[0][3])
    code_list = mongodb.find_item({}, db_name, "code_info")
    target_code = set(item["단축코드"] for item in code_list)
    today = datetime.today().strftime("%Y%m%d")
    print(today)

    collect_list = mongodb.find_item({"날짜:": today}, db_name, "price_info").distinct("code")
    for col in collect_list:
        target_code.remove(col)

    for code in target_code:
        print(code)
        result_credit = ebest.get_credit_trend_by_code(code, today)
        if len(result_credit) > 0:
            mongodb.insert_item_many(result_credit, "stocklab_ace", "credit_info")

def collect_credit_info():
    print(inspect.stack()[0][3])
    code_list = mongodb.find_item({}, db_name, "code_info")
    target_code = set(item["단축코드"] for item in code_list)
    today = datetime.today().strftime("%Y%m%d")
    print(today)

    collect_list = mongodb.find_item({"날짜:": today}, db_name, "price_info").distinct("code")
    for col in collect_list:
        target_code.remove(col)

    for code in target_code:
        print(code)
        result_credit = ebest.get_credit_trend_by_code(code, today)
        if len(result_credit) > 0:
            mongodb.insert_item_many(result_credit, "stocklab_ace", "credit_info")

def collect_stock_info():
    ebest = EBest("DEMO")
    mongodb = MongoDBHandler()
    ebest.login()

    code_list = mongodb.find_item({}, "stocklab_ace", "code_info")
    target_code = set([item["단축코드"] for item in code_list])
    today = datetime.today().strftime("%Y%m%d")
    print(today)

    collect_list = mongodb.find_item({"날짜": today}, "stocklab_ace", "price_info") \
        .distinct("code")
    for col in collect_list:
        target_code.remove(col)

    for code in target_code:
        time.sleep(1)
        print("code:", code)
        """
        result_price = ebest.get_stock_price_by_code(code, "1")
        if len(result_price) > 0:
            print(result_price)
            mongodb.insert_item_many(result_price, "stocklab_ace", "price_info")
        
        
        result_credit = ebest.get_credit_trend_by_code(code, today)
        if len(result_credit) > 0:
            mongodb.insert_item_many(result_credit, "stocklab_ace", "credit_info")
        """
        result_short = ebest.get_short_trend_by_code(code,
                                                     sdate=today, edate=today)
        if len(result_short) > 0:
            mongodb.insert_item_many(result_short, "stocklab_ace", "short_info")

        result_agent = ebest.get_agent_trend_by_code(code,
                                                     fromdt=today, todt=today)
        if len(result_agent) > 0:
            mongodb.insert_item_many(result_agent, "stocklab_ace", "agent_info")
        #
        ebest.logout()


if __name__ == '__main__':
    #collect_code_list()
    collect_price_info()