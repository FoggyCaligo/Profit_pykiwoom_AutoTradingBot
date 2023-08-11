import sys 
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import datetime

import f_getls as getls








class Hoga(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("주식호가잔량")
        # self.setGeometry(300, 300, 300, 400)
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.connect)
        self.ocx.OnReceiveRealData.connect(self._handler_real_data)
        # 2초 후에 로그인 진행
        QTimer.singleShot(1000 * 2, self.CommmConnect)
        #self.code = "005930"
        # self.codes=getls.getList()
        self.codes = getls.getList2()
       

        self.stocksamount = []
        self.stocksprice = []
        self.middle = 10


    def get_each_amountData(self,code):
        rsult = []
        for i in reversed(range(10)):
            rsult.append(self.GetCommRealData(code,71+i))
        for i in range(10):
            rsult.append(self.GetCommRealData(code,61+i))
        return rsult
    def init_each_priceData(self,code):
        rsult = []
        for i in reversed(range(10)):
            rsult.append(self.GetCommRealData(code,51+i))
        for i in range(10):
            rsult.append(self.GetCommRealData(code,41+i))
        return rsult

        
    def _handler_real_data(self, code, real_type, data):
        # print(amountarr)
        # print(pricearr)

        for each in self.codes:
            amountarr = self.get_each_amountData(each)
            pricearr = self.init_each_priceData(each)
            self.stocksamount.append(amountarr)
            self.stocksprice.append(pricearr)

        # print(self.stocksamount)
        # print(self.stocksprice) 

        


    def connect(self):
        self.SetRealReg("1000",self.codes, "41", 0)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Hoga()
    window.show()
    app.exec_()


