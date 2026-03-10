import pandas_datareader.data as web
import datetime as dt
import pandas as pd
import FinanceDataReader as fdr

sp500 = fdr.StockListing('S&P500')['Symbol']#!오류아님. 인덱스에 문자 들어가서 그런거임


stocks=sp500[:10]

df = pd.concat([web.DataReader(stock,'stooq')[:1] for stock in stocks]).reset_index()
print(df)