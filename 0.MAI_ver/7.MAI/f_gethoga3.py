import sys 
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import datetime



import f_getls as getls








class Hoga(QMainWindow):
     #생성자()-----------------------
    def __init__(self):
        super().__init__()
        self.setWindowTitle("주식호가잔량")
        self.setGeometry(300, 300, 300, 400)
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.connect)
        self.ocx.OnReceiveRealData.connect(self._handler_real_data)
        QTimer.singleShot(1000 * 2, self.CommmConnect)

         #변수선언
        self.stocks=[]
        
        #거래할 종목들 코드리스트 받아오기
        #zero
        self.codes = getls.getList2()       
        

    #실시간 실행 함수-------------------
    def _handler_real_data(self):
            print("handler")
            #self.first_get_hoga()#self.stocks 초기화




#순서도 대로 기능 정리한 함수들-------------------------------------------------------------------------------------
    def first_get_hoga(self):
        for each in self.codes:
            print(each)
            self.stocks.append(self.get_each_stock_data(each))
        #print(self.stocks)

    def second_get_future_price(self):

        pass


    def third_order(self):

        pass


    #기능함수 1 : 입력 코드에 해당하는 종목의 호가 데이터 가져오기-----------
    def get_each_stock_data(self,code):
        rsult = []
        temp_amount = []
        temp_price=[]
        for i in reversed(range(10)):
            temp_amount.append(self.GetCommRealData(code,71+i))
            print(self.GetCommRealData(code,71,i))
            temp_price.append(self.GetCommRealData(code,51+i))
        for i in range(10):
            temp_amount.append(self.GetCommRealData(code,61+i))
            temp_price.append(self.GetCommRealData(code,41+i))
        rsult.append(code)
        rsult.append(temp_amount)
        rsult.append(temp_price)
        print(rsult)
        return rsult
        #[종목명, [호가잔량리스트], [호가리스트]]








#기타 필요한 함수들------------------------------------
    def connect(self):
        strarr = ""
        for each in self.codes:
            strarr += each+":"
        strarr = strarr[:-1]
        self.SetRealReg("1000",strarr, "41", 0)

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


