import FinanceDataReader as fdr
import datetime as dt
import c_stock as Stock



def get_PriceData(ksp_num):#최근 2년 하루단위 종가를 반환하는 함수
    return fdr.DataReader(symbol=str(ksp200['Code'][ksp_num]),start=str(dt.date.today().year-1))['Close'].values
def get_name(ksp_num):
    return ksp200['Name'][ksp_num]
def get_code(ksp_num):
    return ksp200['Code'][ksp_num]

def get_PriceYesterday(ksp_num):
    yesterday = dt.date.today()-dt.timedelta(days=1)
    return int(fdr.DataReader(symbol=str(ksp200['Code'][ksp_num]),start=yesterday.strftime('%Y/%m/%d'))['Close'].values[0])


def is_under(price):
    return price<50000
#코스피200종목 뽑기
df_krx = fdr.StockListing('KRX')
ksp200 = df_krx[0:199].copy()#코스피 200 종목 담긴 배열

#print(ksp200['Close'])



#가격이 5만원 이하인 종목들 찾기
under5ls = []
for i in range(199):
    under5ls.append(get_PriceData)






index = 0




stockls = []
for i in ksp200:
    tempc = Class()






def Stockls_refine():



    pass

