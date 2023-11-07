import FinanceDataReader as fdr



df = fdr.StockListing('S&P500')



print(df)


def getList():
    for each in df:
        each = str(each)
        currprice = fdr.DataReader(symbol=each,)

