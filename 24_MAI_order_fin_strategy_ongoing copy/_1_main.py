from multiprocessing import managers
import sys 
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

import pythoncom
import time
import _3_f_getdict as getdict

from pykiwoom.kiwoom import *
import _2_stockManager as manager

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
        self.budjet = 1000000
        #거래할 종목들 코드리스트 받아오기
        self.codes = getdict.getls() 
        #주식 매니저 리스트
        self.managers = []
        for each in self.codes:
            self.managers.append(manager.StockManager(each))
        self.account_no = "8062866811"
        
        #필요한 딕셔너리들
        self.buyprices = {}
        self.predprices = {}
        self.haveamounts = {}
        
        #딕셔너리들 0으로 초기화
        for each in self.codes:
            self.buyprices[each] = 0
            self.predprices[each]=0
            self.haveamounts[each]=0

    #실행함수#----------------------------------------------------------------
    def _handler_real_data(self,code,real_type,data):
        print(code)
        self.buy('005930',1,20000)

        if real_type == "주식호가잔량": #장 중이면---
            hoga = self.get_each_stock_data(code)
            if time.localtime().tm_hour == 15:
                #모두 매도
                for each in self.codes:
                    if self.haveamounts[each] != 0:
                        curr_price = hoga[2][int(len(hoga[1])/2)]
                        self.sell(each,self.haveamounts[each],curr_price)

                pass
                return
            #buy decision
            if self.haveamounts[code] == 0:
                # if(self.calc_rev(hoga[1],hoga[2])!=0):
                    curr_price = (hoga[2][int(len(hoga[1])/2)])
                    print("curr_price:",curr_price)
                    self.haveamounts[code] = (self.budjet/10/int(curr_price))
                    self.predprices[code] = hoga[2][self.predict_priceidx(hoga[2])]            
                    predprice = (self.predprices[code])
                    print("pred_price:",self.predprices[code])
        
                    # tax = predprice*0.0315
                    print("rev:",predprice-curr_price)
                    print("2%:",curr_price*0.7/100)#0.7% 수익 나면
                    if(float(predprice - curr_price) > float(curr_price)/0.7*100.0):#0.7% 수익 나면
                        
                        self.buyprices[code]=curr_price
                        self.buy(code,self.haveamounts[code],curr_price)
                        print(code,": buy")
            #sell decision
            if self.haveamounts[code] != 0:
                curr_price = hoga[2][int(len(hoga[1])/2)]
                print("curr_price:",curr_price)
                if curr_price >= self.predprices[code]:
                    self.sell(code,self.haveamounts[code],curr_price)
                    self.haveamounts[code] = 0
                    print(code,": sell")

            print("--------------------------------")
        else: print("장 안열림")
        #----------------------------------------------------------------
        pass

    #매수/매도 함수
    def buy(self,code,Qty,price):
        self.SendOrder(1,code,Qty,price)
    def sell(self,code,Qty,price):
        self.SendOrder(2,code,Qty,price)
    def SendOrder(self, order_type, code, quantity, price):
        self.ocx.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", 
                                   ["지정가매수", "1000", self.account_no, order_type, code, quantity, price, '00', ""])

    #가격 예측 함수 : 호가리스트의 해당 인덱스 반환
    def predict_priceidx(self,hoga_arr):
        hoga_arri = []
        for i in hoga_arr:
            hoga_arri.append(int(i))

        middle = int(len(hoga_arri)/2)
        buyidx = middle
        sellidx = middle+1
        while(True):
            if(buyidx==0):break
            elif sellidx==len(hoga_arri):break
            if(hoga_arri[buyidx] > hoga_arri[sellidx]):
                hoga_arri[buyidx]-= hoga_arri[sellidx]
                sellidx+=1
            elif(hoga_arri[buyidx]<hoga_arri[sellidx]):
                hoga_arri[sellidx]-=hoga_arri[buyidx]
                buyidx-=1
            else:
                buyidx-=1
                sellidx+=1
        rsult = int((sellidx+buyidx)/2)
        return rsult
        

    # def calc_rev(self,hoga_arr,price_arr):
    #     expec = self.predict_priceidx(price_arr)
    #     middle = int(len(hoga_arr)/2)
    #     if(expec<middle):
    #         return 0
    #     elif middle<expec:
    #         price_arri = []
    #         for i in price_arr:
    #             price_arri.append(int(i))
    #         expec_price = price_arri[expec]
    #         middle_price = price_arri[middle]
    #         revenue=expec_price - middle_price
    #         tax = revenue*0.0315
    #         revenue -= tax
    #         if(revenue>10):
    #             return expec_price
    #         else:return 0

    #호가 가져와서 반환하는 함수
    def get_each_stock_data(self,code):
        rsult = []
        temp_amount = []
        temp_price=[]
        for i in reversed(range(10)):
            temp_amount.append(abs(int(self.GetCommRealData(code,71+i))))#매수호가
            temp_price.append(abs(int(self.GetCommRealData(code,51+i))))#매수수량
        for i in range(10):
            temp_amount.append(abs(int(self.GetCommRealData(code,61+i))))#매도호가
            temp_price.append(abs(int(self.GetCommRealData(code,41+i))))#매도수량
        rsult.append(code)
        rsult.append(temp_amount)
        rsult.append(temp_price)
        print(rsult)
        return rsult# [종목코드, [호가잔량],[호가] ]    ,

#기타 프로그램 돌리는 데 필요한 함수들------------------------------------
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


