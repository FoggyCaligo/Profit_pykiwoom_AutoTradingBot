from pykiwoom.kiwoom import *




kiwoom=Kiwoom()
kiwoom.CommConnect(block=True)
state = kiwoom.GetConnectState()
account = kiwoom.GetLoginInfo("ACCNO")[1]#내 계좌 중 2번째 계좌  불러오기
if(state==0):
    print("연결안됨")
elif state==1:
    print("연결완료")

#매수
def buy(StockCode, Qty, Price):
    kiwoom.SendOrder("","0000",account, 1,StockCode,Qty,Price,'00',"")#주문이름,화면명,계좌번호,주문유형(1매수2매도3매수취소4매도취소5매수정정6매도정정),주식종목코드,주문수량,주문단가,'00':지정가'03':시장가,원주문번호로 주문 정정시 사용. 디폴트 : ""   
#매도
def sell(StockCode, Qty, Price):
    kiwoom.SendOrder("","0000",account, 2,StockCode,Qty,Price,'00',"")



