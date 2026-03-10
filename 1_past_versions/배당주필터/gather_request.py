

from bs4 import BeautifulSoup as bs
import urllib
import time
import requests

import FinanceDataReader as fdr;


def get_dividend_data(ticker):
    data=[]
    url = "https://finance.yahoo.com/quote/"+ticker+"?p="+ticker
    spans = bs(requests.get(url).content,'html.parser').findAll("span")
    rows = bs(requests.get(url).content,'html.parser').findAll("table")[1].tbody.findAll('tr')
    stock_price=0
    #get stock price
    for span in spans:
        if 'Trsdu(0.3s) Fw(b)' in str(span):
            stock_price = float(span.text)
            #print(span.text)
    #get devidend data
    for each_row in rows:
        divs = each_row.findAll('td')
        if 'Forward Dividend' in str(divs[0]):
            #print(divs[1].text)
            div_and_yield = divs[1].text
            dividend,div_yield=div_and_yield.split(" ")
            a = div_yield.replace("(","")
            b = a.replace(")","")
            data.append([float(dividend),str(b)])
        elif 'Ex-Dividend' in str(divs[0]):
            #print(divs[1].text)
            exdate = divs[1].text
    return stock_price,data,exdate


'''
tickers=['CAH','JPM','ABBV','WRK','INTC','KR','TGT','PLD']
rows = []
for ticker in tickers:
    print(ticker)
    stock_price,dividend_data,exdate = get_dividend_data(ticker)
    row = [ticker,dividend_data[0][0], dividend_data[0][1], round(stock_price,2),exdate]
    rows.append(row)
    #일반 유저인척 
    time.sleep(0.5)
'''

sp500 = fdr.StockListing('S&P500')['Symbol']#!오류아님. 인덱스에 문자 들어가서 그런거임
for each in sp500:
    print(each)


rows = []



