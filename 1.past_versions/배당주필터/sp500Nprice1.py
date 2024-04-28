from xml.etree.ElementTree import tostring
import FinanceDataReader as fdr
import pandas_datareader as pdr
import time
import pandas as pd


sp500 = fdr.StockListing('S&P500')['Symbol']#!오류아님. 인덱스에 문자 들어가서 그런거임
code_dict = {}

for each in sp500:
    try:
        date = str(time.localtime().tm_year)+str(time.localtime().tm_mon)+str(time.localtime().tm_mday-3)
        price = fdr.DataReader(symbol=each,start=date)['Close'][-1]
        if(price<30):
            code_dict[each]=price
            print(each,price)
    except:
        continue


pd.DataFrame(code_dict).to_csv('./trade_record.csv')
print(code_dict)
