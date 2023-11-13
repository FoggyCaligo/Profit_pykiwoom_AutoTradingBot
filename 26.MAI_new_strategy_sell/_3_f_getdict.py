import FinanceDataReader as fdr
import datetime as dt
import numpy as np


df_kospi = fdr.StockListing('KOSPI')
ks200 = df_kospi[:]
# print(ks200)



stockdict = {}

def getdict ():
    for each in range(len(ks200['Code'])):
        currprice = ks200['Open'][each]
        if(10000<currprice and currprice<50000):
            stockdict[ks200['Code'][each]] = currprice
    print(stockdict)
    return stockdict


#print(ks200)

stockls = []
def getls():
    for each in range(len(ks200['Code'])):
        currprice = ks200['Open'][each]
        if(10000<currprice and currprice<50000):
            stockls.append(ks200['Code'][each])
            # stockdict[ks200['Code'][each]] = currprice
            print(ks200['Code'][each])
    return stockls[:]



value = getls()
#print(value)