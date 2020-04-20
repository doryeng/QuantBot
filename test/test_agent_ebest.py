import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from stocklab.agent.ebest import EBest

import unittest
import inspect
import time

class TestEBest(unittest.TestCase):
    def setUp(self):
        self.ebest = EBest("DEMO")
        self.ebest.login()

    def tearDown(self):
        self.ebest.logout()

    """
    def test_get_code_list(self):
        print(inspect.stack()[0][3])
        all_result = self.ebest.get_code_list("ALL")
        assert all_result is not None
        kosdaq_result = self.ebest.get_code_list("KOSDAQ")
        assert kosdaq_result is not None
        kospi_result = self.ebest.get_code_list("KOSPI")
        assert kospi_result is not None
        try:
            error_result = self.ebest.get_code_list("KOS")
        except:
            error_result = None
        assert error_result is None
        print("result:", len(all_result), len(kosdaq_result), len(kospi_result))

    def test_get_stock_price_by_code(self):
        print(inspect.stack()[0][3])
        result = self.ebest.get_stock_price_by_code("005930","2")
        assert result is not None
        print(result)

    def test_agent_account_info(self):
        result = self.ebest.get_account_info()
        assert result is not None
        print(result)

    def test_agent_account_stock_info(self):
        result = self.ebest.get_accout_stock_info()
        assert result is not None
        print(result)


    def test_order_stock(self):
        print(inspect.stack() [0][3])
        result = self.ebest.order_stock("005930", "2", "48000", "2", "00")
        assert result
        print(result)

    def test_order_cancel(self):
        print(inspect.stack()[0][3])
        result = self.ebest.order_cancel("32957", "A005930", "1")
        assert result
        print(result)

    def test_order_check(self):
        print(inspect.stack()[0][3])
        result = self.ebest.order_check("32957")
        assert result
        print(result)

    def test_get_current_call_price_by_code(self):
        print(inspect.stack()[0][3])
        result = self.ebest.get_current_call_price_by_code("005930")
        assert result
        print(result)

    def test_get_price_n_min_by_code(self):
        print(inspect.stack()[0][3])
        result = self.ebest.get_price_n_min_by_code("20190412", "180640")
        assert result
        print(result)
    """
    """
    
    
    def test_get_price_n_min_by_code_tick(self):
        print(inspect.stack()[0][3])
        result = self.ebest.get_price_n_min_by_code("20200412", "005930", 0)
        assert result
        print(result)
    """