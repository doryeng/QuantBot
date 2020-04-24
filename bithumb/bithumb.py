from urllib.request import urlopen
import json
from field import Field

class Bithumb:
    def _query(self, tickers):
        i = 0
        for item in tickers:
            if getattr(Field, "ticker", None):
                res_field = getattr(Field, "ticker", None)
                if item in res_field:
                    field_hname = res_field[item]
                    tickers[i] = field_hname
            i += 1
        return tickers

    def tickers(self):
        uri = "https://api.bithumb.com/public/ticker/{}_{}".format("ALL", "KRW")
        responseBody = urlopen(uri).read().decode('utf-8')
        jsonArray = json.loads(responseBody)
        DataArray = jsonArray.get("data")
        tickers = [k for k, v in DataArray.items() if isinstance(v, dict)]
        for item in tickers:
            print("item :",item)
            DataArray[item] = "헤헤"
        result = self._query(tickers)
        return DataArray

    def tickers2(self):
        uri = "https://api.bithumb.com/public/ticker/{}_{}".format("ALL", "KRW")
        responseBody = urlopen(uri).read().decode('utf-8')
        jsonArray = json.loads(responseBody)
        DataArray = jsonArray.get("data")
        tickers = [k for k, v in DataArray.items() if isinstance(v, dict)]
        for item in tickers:
            datas = DataArray.get(item)
            names = [k for k, v in datas.items() if isinstance(v, str)]
            print(names)

bithumb = Bithumb()
result = bithumb.tickers()
print(result)
#bithumb.tickers2()
