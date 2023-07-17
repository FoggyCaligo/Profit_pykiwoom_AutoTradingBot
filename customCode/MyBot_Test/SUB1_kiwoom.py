from pykiwoom.kiwoom import *

#접속
kiwoom=Kiwoom()
kiwoom.CommConnect(block=True)




#유저 정보 불러오기
account_num = kiwoom.GetLoginInfo("ACCOUNT_CNT") #전체 계좌 수
accounts=kiwoom.GetLoginInfo("ACCNO")#전체 계좌 리스트
user_id = kiwoom.GetLoginInfo("USER_ID")
user_name = kiwoom.GetLoginInfo("USER_NAME")
keyboard = kiwoom.GetLoginInfo("KEY_BSECGB")#키보드보안 해지여부
firewall = kiwoom.GetLoginInfo("FIREW_SECGB")

account = accounts[1]
print(account)



state = kiwoom.GetConnectState()
if(state==0):
    print("연결안됨")
elif state==1:
    print("연결완료")


def buy(StockCode, Qty, Price):
    kiwoom.SendOrder("","0000",account, 1,StockCode,Qty,Price,'00',"")#주문이름,화면명,계좌번호,주문유형(1매수2매도3매수취소4매도취소5매수정정6매도정정),주식종목코드,주문수량,주문단가,'00':지정가'03':시장가,원주문번호로 주문 정정시 사용. 디폴트 : ""   
def sell(StockCode, Qty, Price):
    kiwoom.SendOrder("","0000",account, 2,StockCode,Qty,Price,'00',"")

#------------------------



def order(type, StockCode, Qty,Price, order_no):
    kiwoom.SendOrder("","0101",str(accounts[1]), type,StockCode,Qty,Price,'00',order_no)#주문이름,화면명,계좌번호,주문유형(1매수2매도3매수취소4매도취소5매수정정6매도정정),주식종목코드,주문수량,주문단가,'00':지정가'03':시장가,원주문번호로 주문 정정시 사용. 디폴트 : ""
    #type,code,qty,price,order_no
    
def get_orders():
    kiwoom.SetInputValue(account)




#print(kiwoom.SendOrder("","0101",str(accounts[1]), 2,"005930",1,50000,'00',""))

def get_Orders():
    pass






