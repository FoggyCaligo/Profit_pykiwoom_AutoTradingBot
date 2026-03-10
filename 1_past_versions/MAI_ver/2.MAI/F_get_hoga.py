import sys 
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import datetime
from pykiwoom.kiwoom import *
#jay
import F_getkospi100 as getls


class HogaManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("주식호가잔량")
        # self.setGeometry(300, 300, 300, 400)
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.connect)
        self.ocx.OnReceiveRealData.connect(self._handler_real_data)
        # 2초 후에 로그인 진행
        QTimer.singleShot(1000 * 2, self.CommmConnect)

        #s내 종목들 배열 
        self.codels = getls.getList()#코스피200중 가격 낮은 종목 리스트 가져오기
        print('init',self.codels)
        self.datas = []


        

    def _handler_real_data(self):
        price = self.GetCommRealData(self.code,41)
        print(price)
    









#필요한 함수들
    def connect(self):
        self.SetRealReg("1000", self.codels, "41", 0)
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
    window = HogaManager()
    window.show()
    app.exec_()