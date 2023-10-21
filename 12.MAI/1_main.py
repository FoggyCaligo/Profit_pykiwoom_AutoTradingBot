import sys 
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import datetime

import f_getls as getls
import f_logic as logic
import f_order as order


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
        self.currPricedict = getls.getdict()  
        self.expecPricedict = {}

        self.stocklsamount = len(self.expecPricedict)
        
    #실행함수
    def _handler_real_data(self,code,real_type,data):
        if real_type == "장시작시간":#장 시작 전--------------------------------
            
            
            pass
        elif real_type == "주식호가잔량":#확인 완료-------------------------------------------
            print("장중")
            #정보가져오기 & 예측가 연산
            self.currPricedict[code] = self.get_each_stock_data(code)#현재 호가 가져오기
            self.expecPricedict[code] = logic.calc_assumePriceIndex(int(self.currPricedict[code]))#예상가 연산해서 가져오기
            #매수판단
            curr_price = len(self.currPricedict)/2
            if self.expecPricedict[code] > self.currPricedict[code][curr_price] + curr_price*2/1000 + curr_price*15/10000 + curr_price*2/100:#예상가 > 현재가+세금(0.2%)+수수료(0.015%)+2%수익
                #order.buy(code, ,curr_price)
                # -> 매수 수량을 정하는 알고리즘 필요

                pass
            #매도판단

            print('\n')

        elif real_type == "장종료10분전동시호가":#장 종료 10분전 동시호가---------
            print("10분 전!")



            
        else :#-----------------------------------------------------------
            print("장 열리지 않음",real_type)

        




        # self.first_get_hoga()

        # for each in self.stocks:
        #     print("종목:",each,"\n")
        # print('\nㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        

        # self.second_get_future_price()








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


