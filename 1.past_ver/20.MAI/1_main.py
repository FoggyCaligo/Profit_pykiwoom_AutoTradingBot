import sys 
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import datetime

import f_getdict as getdict
import f_logic_cp as logic
import time

import stockManager as manager

# import f_order as order

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

         #변수선언
        self.stocks=[]#  [   [종목코드, [호가잔량],[호가] ]    ,
        self.tradingstocks = [] #[[종목명,기대주가,당시시가(중간가격)]]
        
        #거래할 종목들 코드리스트 받아오기
        # self.codes = getls.getList() 
        self.codes = getdict.getls()  

    #실행함수#----------------------------------------------------------------
    def _handler_real_data(self,code,real_type,data):
        #호가 확인
        print("handler")
        self.first_get_hoga()
        for each in self.stocks:
            print("종목:",each,"\n")
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        
        print(real_type)
        
        if(real_type == "주식호가잔량"):
            print("장중")
            now = time.localtime()
            if(now.tm_hour==15):#장마감30분전
                #sell_ all
                
                pass
            else:#장중
                for each in self.manager:
                    hoga = self.get_each_stock_data(each.get_code())
                    each.buy(hoga[2],hoga[1])
                    print(hoga[0],"buy")
                for each in self.manager:
                    hoga = self.get_each_stock_data(each.get_code())
                    each.sell(hoga[2],hoga[1])
                    print(hoga[0],"sell")
        else:
            print("장 아님")
            pass








        #----------------------------------------------------------------
        pass


#순서대로
    def first_get_hoga(self):
        self.stocks.clear()
        for each in self.codes:
            self.stocks.append(self.get_each_stock_data(each))

    def second_get_future_price(self):
        self.tradingstocks.clear()
        for each_stock in self.stocks: #[   [종목코드, [호가잔량],[호가] ]    ,[종목코드, [호가잔량],[호가]].. ]
            temp = []
            expec_price_index = logic.calc_assumePriceIndex(int(each_stock[1]))
            if expec_price_index == 0 : continue#수익 리턴이 0이 나오면 제끼기
            middle_price = each_stock[2][int(len(each_stock[2])/2)]
            expec_price = each_stock[2][expec_price_index]
            temp.append(each_stock[0])
            temp.append(expec_price)
            temp.append(middle_price)
            self.tradingstocks.append(temp)
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


