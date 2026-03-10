import sys 
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import datetime

import pythoncom
import time
import _3_f_getdict as getdict

from pykiwoom.kiwoom import *

class Main(QMainWindow):
    #생성자
    def __init__(self):
        # kiwoom = Kiwoom()
        # kiwoom.CommConnect()
        # self.account_no = kiwoom.GetLoginInfo("ACCNO")
        


        super().__init__()
        self.setWindowTitle("주식호가잔량")
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.connect)
        self.ocx.OnReceiveRealData.connect(self._handler_real_data)
        QTimer.singleShot(1000 * 2, self.CommConnect)
         #변수선언
        
        #거래할 종목들 코드리스트 받아오기
        self.codes = getdict.getls() 


        self.account_no = "8062866811"

        


    #실행함수#----------------------------------------------------------------
    def _handler_real_data(self,code,real_type,data):
        print(code)
        # print(self.account)
        self.buy(code,1,200000)

        



        #----------------------------------------------------------------
        pass


#순서대로

    def buy(self,code,Qty,price):
        self.SendOrder(1,code,Qty,price)
    def sell(self,code,Qty,price):
        self.SendOrder(2,code,Qty,price)
    

    def SendOrder(self, order_type, code, quantity, price):
        self.ocx.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", 
                                   ["지정가매수", "0000", self.account_no, order_type, code, quantity, price, '00', ""])

    


    def get_each_stock_data(self,code):
        rsult = []
        temp_amount = []
        temp_price=[]
        for i in reversed(range(10)):
            temp_amount.append(self.GetCommRealData(code,71+i))#매수호가
            temp_price.append(self.GetCommRealData(code,51+i))#매수수량
        for i in range(10):
            temp_amount.append(self.GetCommRealData(code,61+i))#매도호가
            temp_price.append(self.GetCommRealData(code,41+i))#매도수량
        rsult.append(code)
        rsult.append(temp_amount)
        rsult.append(temp_price)
        return rsult

#기타 필요한 함수들------------------------------------
    def connect(self):
        strarr = ""
        for each in self.codes:
            strarr += each+";"
        strarr = strarr[:-1]
        self.SetRealReg("1000",strarr, "41", 0)
    def CommConnect(self):
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()


