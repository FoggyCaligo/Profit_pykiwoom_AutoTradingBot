import FinanceDataReader as fdr
import pandas_datareader as pdr
import time
import pandas as pd

sp500 = fdr.StockListing('S&P500')['Symbol']#!오류아님. 인덱스에 문자 들어가서 그런거임

code_dict = {}

df = pdr.get_data_stooq(sp500[0])
print(df)

for each in sp500:
    try:
        price = pdr.get_data_fred(each)['Close'][-1]
        print(price)
        if(price<30):
            code_dict[each]=price
            print(each,price)
    except:
        continue


pd.DataFrame(code_dict).to_csv('./trade_record.csv',index=False)
print(code_dict)

