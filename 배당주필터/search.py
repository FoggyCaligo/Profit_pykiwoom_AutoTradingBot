import FinanceDataReader as fdr
import time


df = fdr.StockListing('S&P500')
# print(df)


print(df)

# for i in df["Symbol"]:
#     print(i)







# getList()
class Filter:
    def __init__(self):
        self.df = fdr.StockListing('S&P500')
        self.stockdict = {}
        for each in self.df['Symbol']:
            # print(type(time.localtime().tm_year))
            price = fdr.DataReader(each,str(time.localtime().tm_year))
            price = price.head(1)
            self.stockdict[each]=price

    def filter_price(self,startprice,endprice):
        for each in range(len(self.df['Symbol'])):
            currprice = self.df['Open'][each]
            print(currprice)
            if(startprice<currprice and currprice<endprice):
                self.stockdict[self.df['Symbol'][each]] = currprice
        print(self.stockdict)
        return self.stockdict
    


filter = Filter()
# filter.filter_price(0,20000)