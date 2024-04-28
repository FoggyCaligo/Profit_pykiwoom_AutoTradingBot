#정보탐색 기능파일.py
from Basic_Functions import Functions as funcs
#최근 2년간의 하루단위 종가를 배열로 불러오는 함수
arr = funcs.get_PriceData(0) #arr에 종가배열 저장됨


#실제 거래 담당 기능파일.py
import SUB1_kiwoom as kiwoom
#kiwoom.order(1,funcs.get_code(0),1,funcs.get_PriceYesterday(0)["Close"],"")
kiwoom.buy(funcs.get_code(0),1,funcs.get_PriceYesterday(0)-1000)
kiwoom.buy(funcs.get_code(0),1,60000)


print(funcs.get_PriceYesterday(0))
print("주문완료")


#CLASS Convert test--------------------------------------
order = kiwoom.Order()
order.get_hoga(funcs.get_code(0))



#---------------------------------------------------------------






