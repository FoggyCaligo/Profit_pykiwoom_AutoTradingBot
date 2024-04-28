import FinanceDataReader as fdr

df_krx = fdr.StockListing('KRX')
#코스피 200 구성종목들이 담겨있는 배열 DataArr
DataArr = df_krx[0:199] 
print(DataArr)



for each in DataArr:
    chart = fdr.DataReader(Symbol=each
    

