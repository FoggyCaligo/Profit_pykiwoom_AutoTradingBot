import FinanceDataReader as fdr
import datetime as dt
import numpy as np


df_kospi = fdr.StockListing('KOSPI')
ks200 = df_kospi[:70]
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


value = getdict()
#print(value)