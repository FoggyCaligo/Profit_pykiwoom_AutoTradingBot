import sys 
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import datetime

import f_getls as getls
import f_logic_fin as logic


from pykiwoom.kiwoom import *


class Hoga(QMainWindow):

    #초기화 함수
    def __init__(self):

        #변수 선언
        self.codes = getls.getList2()
        # self.input = 1000000    #(백만) -> 모의투자용 테스트. 실전에서는 운용 자금만큼.
        


        super().__init__()
        self.setWindowTitle("주식")
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.connect)
        self.ocx.OnReceiveRealData.connect(self.handler_real_data)
        QTimer.singleShot(1000*2,self.CommConnect)

    def handler_real_data(self,code,real_type, data):
            # print("handler")

            # while(True):
            #     self.first_get_hoga()
            #     if(self.stocks[0][1][0] != ''):
            #         self.second_get_future_price()
            #     else:
            #         print("market not opened yet")
            print("handler")
        

    









        
#  기타 함수
    def connect(self):
        self.SetRealReg("1000", "005930", "41", 0)

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
