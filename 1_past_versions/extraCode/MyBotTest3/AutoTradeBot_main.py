import sys 
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import datetime
import F_Order as order

from pykiwoom.kiwoom import *




class StockBot_MK1(QMainWindow):
    
    def __init__(self):
        #호가정보통신연결
        super().__init__()
        self.setWindowTitle("주식봇 MAI")
        self.setGeometry(300,300,500)
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.connect)
        self.ocx.OnReceiveRealData.connect(self._handler_real_data)
        QTimer.singleShot(1000 * 2, self.CommmConnect)
        #주문통신연결
        self.kiwoom=Kiwoom()
        self.kiwoom.CommConnect(block=True)
        state = self.kiwoom.GetConnectState()
        account = self.kiwoom.GetLoginInfo("ACCNO")[1]#내 계좌 중 2번째 계좌  불러오기

        #내 변수들


        
    #매수
    def buy(self,StockCode, Qty, Price):
        self.kiwoom.SendOrder("","0000",account, 1,StockCode,Qty,Price,'00',"")#주문이름,화면명,계좌번호,주문유형(1매수2매도3매수취소4매도취소5매수정정6매도정정),주식종목코드,주문수량,주문단가,'00':지정가'03':시장가,원주문번호로 주문 정정시 사용. 디폴트 : ""   
    #매도
    def sell(self,StockCode, Qty, Price):
        self.kiwoom.SendOrder("","0000",account, 2,StockCode,Qty,Price,'00',"")


    def on_hogaUpdate(self):
        pass


    #호가연결
    def connect(self):
        self.SetRealReg("1000", self.code, "41", 0)
    def CommmConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        self.statusBar().showMessage("login 중 ...")
    def SetRealReg(self, screen_no, code_list, fid_list, real_type):
        self.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)", 
                              screen_no, code_list, fid_list, real_type)
        self.statusBar().showMessage("구독 신청 완료")
    def DisConnectRealData(self, screen_no):
        self.ocx.dynamicCall("DisConnectRealData(QString)", screen_no)
        self.statusBar().showMessage("구독 해지 완료")
    def GetCommRealData(self, code, fid):
        data = self.ocx.dynamicCall("GetCommRealData(QString, int)", code, fid) 
        return data
    def __del__(self):
        self.DisConnectRealData("1000")     
