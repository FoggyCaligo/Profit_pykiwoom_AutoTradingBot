from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

import FinanceDataReader as fdr
import time



# 가격 필터(s&p 500종목에서 x달러 이하인 종목만 가져오기)
# 현재 월 기준 배당락일 1개월 이내인 종목 가져오기
# sp_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
# sp500_constituents = pd.read_html(sp_url, header=0)[0]
# sp500_constituents.info()

code_dict = {}

def get_sp500():
    df = fdr.StockListing('S&P500')
    count = 0
    for each in df['Symbol']:
        try:
            price = fdr.DataReader(each,str(time.localtime().tm_year)+'-'+str(time.localtime().tm_mon)).tail(2)['Close'][0]# 해당 년도의 주가 전부 가져오기
            if price < 30: 
                code_dict[each]= price
                print(each,price)
            count+=1
        except:
            continue
    print(code_dict)
    print(count)

get_sp500()