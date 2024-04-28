import sys 
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import datetime

# import f_getls as getls
import f_logic as logic

import f_getdict as getdict

# from pykiwoom.kiwoom import *


class Main(QMainWindow):
    #생성자
    def __init__(self):
        super().__init__()
        self.setWindowTitle("주식호가잔량")
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.connect)
        self.ocx.OnReceiveRealData.connect(self._handler_real_data)
        QTimer.singleShot(1000 * 2, self.CommConnect)
        #거래할 종목들 코드리스트 받아오기
        # self.codes = getls.getList()   

        self.codedict = getdict.getdict()

        print("test1")
    #실행함수
    def _handler_real_data(self,code,real_type,data):
        print("test2")

        print(real_type)
        
        if real_type == "장시작시간":#장 시작 전--------------------------------
            print("장시작시간")
            
            pass
        elif real_type == "주식호가잔량":#확인 완료-------------------------------------------
            print("장중")
            

            # print(data)
            # print('\n')
            

        elif real_type == "장종료10분전동시호가":#장 종료 10분전 동시호가---------
            print("10분 전!")
            


            
        else :#-----------------------------------------------------------
            print("장 열리지 않음",real_type)







#기타 필요한 함수들------------------------------------
    def connect(self):
        strarr = ""
        for each in self.codedict:
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


