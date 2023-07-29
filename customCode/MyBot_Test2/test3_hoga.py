import sys 
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import datetime


class MyWindow(QMainWindow):
    code = '005930'



    def __init__(self,code):
        self.code = code
        super().__init__()
        

        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self._handler_login)
        self.ocx.OnReceiveRealData.connect(self._handler_real_data)




        # self.connect()
        # 2초 후에 로그인 진행
        QTimer.singleShot(1000*10,self.connect)
        QTimer.singleShot(1000 * 0, self.CommmConnect)


        self.connect()

    def __del__(self):
         self.DisConnectRealData("1000") 


    def connect(self):
        self.SetRealReg("1000", self.code, "41", 0)
    def disconnect(self):
        self.DisConnectRealData("1000") 



    def CommmConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        self.statusBar().showMessage("login 중 ...")

    def _handler_login(self, err_code):
        if err_code == 0:
            self.statusBar().showMessage("login 완료")


    def _handler_real_data(self, code, real_type, data):
        if real_type == "주식호가잔량":
            hoga_time =  self.GetCommRealData(code, 21)         
            ask01_price =  self.GetCommRealData(code, 41)         
            ask01_volume =  self.GetCommRealData(code, 61)         
            bid01_price =  self.GetCommRealData(code, 51)         
            bid01_volume =  self.GetCommRealData(code, 71)         
            print(hoga_time)
            print(f"매도호가: {ask01_price} - {ask01_volume}")
            print(f"매수호가: {bid01_price} - {bid01_volume}")

    def SetRealReg(self, screen_no, code_list, fid_list, real_type):
        self.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)", 
                              screen_no, code_list, fid_list, real_type)
        print("구독신청 완료")
    def DisConnectRealData(self, screen_no):
        self.ocx.dynamicCall("DisConnectRealData(QString)", screen_no)
        print("구독 해지 완료")
    def GetCommRealData(self, code, fid):
        data = self.ocx.dynamicCall("GetCommRealData(QString, int)", code, fid) 
        return data


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow('005930')
    window.show()
    app.exec_()