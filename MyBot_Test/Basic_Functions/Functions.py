import FinanceDataReader as fdr
import datetime as dt

df_krx = fdr.StockListing('KRX')
KSP200 = df_krx[0:199].copy()#코스피 200 종목 담긴 배열

def get_PriceData(ksp_num):#최근 2년 하루단위 종가를 반환하는 함수
    return fdr.DataReader(symbol=str(KSP200['Code'][ksp_num]),start=str(dt.date.today().year-2))

def get_name(ksp_num):
    return KSP200['Name'][ksp_num]

def get_currPrice(ksp_num):
    pass

