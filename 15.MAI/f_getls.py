import FinanceDataReader as fdr
import datetime as dt
import numpy as np


df_kospi = fdr.StockListing('KOSPI')
ks100 = df_kospi[:100]#코스피 상위 100종목 뽑기


stocklist = []
print(stocklist)


def getList():
    for each in ks100['Code']:
        each = str(each)
        currPrice = (fdr.DataReader(symbol=each,start=str(dt.date.today())))#오늘자 주가 뽑기
        currPrice = int(currPrice['Open'].values)#오늘자 주가 정수형으로 변환
        if(10000<currPrice and currPrice<50000):#만원 이상 5만원 이하인 종목 뽑기
            stocklist.append(each)
            print(each)
        
    print(stocklist)
    return stocklist[:10]#상위 10개 종목 뽑기

# def getList2():
#     data=[]
#     for each in ks100['Code']:
#         each=str(each)
#         currprice = (fdr.DataReader(symbol=each,start=str(dt.date.today())))#오늘자 주가 뽑기
v = getList()
