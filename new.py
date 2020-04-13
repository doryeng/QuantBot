import configparser
"""
import win32com.client
client = win32com.client.Dispatch("XA_Session.XASession")
client.ConnectServer("demo.ebestsec.co.kr",20001)
"""
config = configparser.ConfigParser()
config.read('c://Users/mskwon/Desktop/stock-lab/conf/config.ini')
print(config["EBEST_DEMO"]['user'])
