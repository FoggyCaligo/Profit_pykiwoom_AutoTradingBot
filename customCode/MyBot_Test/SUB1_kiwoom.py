from pykiwoom.kiwoom import *
import SUB1_data as data

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

# def _handler_login(self, err_code):
#         if err_code == 0:
#             self.statusBar().showMessage("login 완료")
# def _handler_real_data(self, code, real_type, data):
#         if real_type == "주식호가잔량":
#             hoga_time =  self.GetCommRealData(code, 21)         
#             ask01_price =  self.GetCommRealData(code, 41)         
#             ask01_volume =  self.GetCommRealData(code, 61)         
#             bid01_price =  self.GetCommRealData(code, 51)         
#             bid01_volume =  self.GetCommRealData(code, 71)   
# def get_hoga(code):
#     kiwoom2 = Kiwoom()
#     kiwoom2.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
#     kiwoom2.ocx.OnEventConnect.connect(_handler_login)
    


#     hoga_time = kiwoom.GetCommRealData(code,21)
#     ask_price= kiwoom.GetCommRealData(code,41)
#     ask_volume = kiwoom.GetCommRealData(code,61)
#     bid_price = kiwoom.GetCommRealData(code,51)
#     bid_volume = kiwoom.GetCommRealData(code,71)
#     print(hoga_time)
#     print(ask_price)
#     print(ask_volume)


# get_hoga(funcs.get_code(0))







#()
def order(type, StockCode, Qty,Price, order_no):
    kiwoom.SendOrder("","0101",str(accounts[1]), type,StockCode,Qty,Price,'00',order_no)#주문이름,화면명,계좌번호,주문유형(1매수2매도3매수취소4매도취소5매수정정6매도정정),주식종목코드,주문수량,주문단가,'00':지정가'03':시장가,원주문번호로 주문 정정시 사용. 디폴트 : ""
    #type,code,qty,price,order_no
    
def get_orders():
    kiwoom.SetInputValue(account)




class Order:
    def __init__(self):
        self.kiwoom = Kiwoom()
        self.kiwoom.CommConnect(block=True)
        accounts1=self.kiwoom.GetLoginInfo("ACCNO")#전체 계좌 리스트
        account1 = accounts1[1]
        state = kiwoom.GetConnectState()
        if(state==0):
            print(" Kiwoom Class 연결안됨")
        elif state==1:
            print("Kiwoom Class 연결완료")

    def get_hoga(self,code):
        hoga_time = self.kiwoom.GetCommRealData(code,21)
        print(hoga_time)




    def buy(StockCode, Qty, Price):
        kiwoom.SendOrder("","0000",account, 1,StockCode,Qty,Price,'00',"")#주문이름,화면명,계좌번호,주문유형(1매수2매도3매수취소4매도취소5매수정정6매도정정),주식종목코드,주문수량,주문단가,'00':지정가'03':시장가,원주문번호로 주문 정정시 사용. 디폴트 : ""   
    def sell(StockCode, Qty, Price):
        kiwoom.SendOrder("","0000",account, 2,StockCode,Qty,Price,'00',"")






