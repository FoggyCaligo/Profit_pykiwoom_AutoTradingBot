import sys 
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import datetime


import class_hogaData as StockClass
import f_getls as getls


class Hoga(QMainWindow):
    
    def __init__(self,code):
        super().__init__()
        self.setWindowTitle("주식호가잔량")
        self.setGeometry(300, 300, 300, 400)
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.connect)
        self.ocx.OnReceiveRealData.connect(self._handler_real_data)
        
        # 2초 후에 로그인 진행
        QTimer.singleShot(1000 * 2, self.CommmConnect)
        self.codes = getls.getList()
        print(self.codes)
        
    def connect(self):
        self.SetRealReg("1000", self.codes, "41", 0)

    def CommmConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        self.statusBar().showMessage("login 중 ...")



    def _handler_real_data(self):
        self.buyamount.clear()
        self.buyprice.clear()
        self.sellamount.clear()
        self.sellprice.clear()
        for eachcode in self.codes:#각각의 종목코드들 순회
            print("종목코드 :",eachcode)
            for i in range(10):#10호가(매수/매도가 층들)
                self.buyammount.append(self.GetCommRealData(eachcode,71+i))
                self.buyamount.append(self.GetCommRealData(eachcode,71+i))
                self.buyprice.append(self.GetCommRealData(eachcode,51+i))
                self.sellamount.append(self.GetCommRealData(eachcode,61+i))
                self.sellprice.append(self.GetCommRealData(eachcode,41+i))
            
        print("--------------------------")
        print(self.buyprice)
        print(self.buyamount)
        print("\n")
        print(self.sellprice)
        print(self.sellamount)
        






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
    window = Hoga("005930")
    window.show()
    app.exec_()
