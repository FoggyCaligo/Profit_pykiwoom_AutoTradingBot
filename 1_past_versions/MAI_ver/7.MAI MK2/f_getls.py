import FinanceDataReader as fdr
import datetime as dt
import numpy as np

df_krx = fdr.StockListing('KRX')
#DataArr = df_krx[0:100].copy()#코스피 200 종목 담긴 배열
DataArr = df_krx[0:100]#코스피 200 종목 담긴 배열


stocklist = []

def f_getPriceData(ksp_num):#최근 2년 하루단위 종가를 반환하는 함수
    return fdr.DataReader(symbol=str(DataArr['Code'][ksp_num]),start=str(dt.date.today().year-2))


#코스피200(100으로 줄임)에서 가격 낮은 종목 추출
def getList():
    for each in DataArr['Code']:
        each = str(each)
        currPrice = (fdr.DataReader(symbol=each,start=str(dt.date.today())))
        # currPrice = (fdr.DataReader(symbol=each,start='2023-08-01',end='2023-08-01'))
        
        currPrice = int(currPrice['Open'].values)


        if currPrice<30000:
            stocklist.append(each)
            print(each)


    
    return stocklist[:5]#상위 5개 종목 뽑기




def getList2():
    data = []
    for each in DataArr['Code']:
        each = str(each)
        currprice = (fdr.DataReader(symbol=each,start=str(dt.date.today())))
        currprice = int(currprice['Open'].values)
        if(currprice<30000):
            temp = []
            temp.append(currprice)
            temp.append(each)
            data.append(temp)
    
    data.sort(key=lambda x:x[0])
    # print(data[0:10][1])
    # print(data[0:10][0])
    rsult = []
    for i in range(10):
        rsult.append(data[i][1])



    print(rsult)
    return rsult



    # print(data)

    return data[1][0:5]
    

