from bithumb import Bithumb
import unittest

class Test(unittest.TestCase):
    def test_bithumb_tickers(self):
        bithumb = Bithumb()
        result = bithumb.tickers()
        print(result)