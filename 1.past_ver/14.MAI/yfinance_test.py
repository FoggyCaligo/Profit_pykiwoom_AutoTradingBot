from pandas_datareader import data as pdr
import yfinance as yf
# yf.pdr_override()

# data = pdr.get_data_yahoo("005930.KS",start="2023-01-01", end = "2023-01-01")
# print(data)




df = yf.download('005930.KS',period='1d')
print(df)
