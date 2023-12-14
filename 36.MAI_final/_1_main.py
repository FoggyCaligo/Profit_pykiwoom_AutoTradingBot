from multiprocessing import managers
import sys 
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import datetime
import pandas as pd
import sys

import pythoncom
import time
import _3_f_getdict as getdict

from pykiwoom.kiwoom import *
import _2_stockManager as manager


class Main(QMainWindow):
    #생성자
    def __init__(self):
        # kiwoom = Kiwoom()
        # kiwoom.CommConnect()
        # self.account_no = kiwoom.GetLoginInfo("ACCNO")
        self.df = pd.read_csv("trade_record.csv")
        self.is_exit = False

        super().__init__()

        self.btn1 = QPushButton('&Button1', self)
        self.btn1.setText('exit')
        self.btn1.setCheckable(True)
        self.btn1.toggle()


        self.setWindowTitle("주식호가잔량")
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.connect)
        self.ocx.OnReceiveRealData.connect(self._handler_real_data)
        self.ocx.OnReceiveChejanData.connect(self._receive_chejan_data)
        self.ocx.OnReceiveTrData.connect(self.tr_slot)
           
        # self.ocx.OnReceiveTrData.connect(self.__tr_1000_slot)
        # self.ocx.tr_1000_event_loop=QEventLoop()
        # self.ocx.tr_1000_event_loop.exec_()
        QTimer.singleShot(1000 * 2, self.CommConnect)
         #변수선언
        
        self.budjet = 1000000

        #거래할 종목들 코드리스트 받아오기
        self.codes = getdict.getls() 
        self.managers = []
        for each in self.codes:
            self.managers.append(manager.StockManager(each))
        # self.account_no = "8063342511"
        self.account_no = "8063880211"
        
        
        self.buyprices = {}
        self.predprices = {}
        self.haveamounts = {}
        self.remainamounts = {}
        self.currprice = {}

        self.remain_buy_orders = {}

        for each in self.codes:
            self.buyprices[each] = 0
            self.predprices[each]=0
            self.haveamounts[each]=0
            self.remainamounts[each]=0
            self.currprice[each] = 0
            self.remain_buy_orders[each] = 0

        self.temp_code = ""
        self.temp_qty = ""
        self.temp_price = ""

        #미체결
        self.account_loop = QEventLoop()                 
        # self.not_signed_account()
        self.is_cleared = False

    
    #실행함수#----------------------------------------------------------------
    def _handler_real_data(self,code,real_type,data):
        
        if real_type == "주식호가잔량": #장 중이면---
            # self.cancel_all_buyorder()
            # if self.is_cleared == False:
            #     self.sell_all_remainings()
            #     self.is_cleared = True

            print(code)
            hoga = self.get_each_stock_data(code)
            # print("type:",type(code))
            #MK2-------------------------------------------------
            curr_price = abs(int(hoga[2][int(len(hoga[1])/2)]))
            pred_price = abs(int(hoga[2][self.predict_priceidx(hoga[1])]))
            qty = abs(int(self.budjet/10/curr_price))

            if pred_price - curr_price > curr_price*0.8/100: #수익률   
                self.buy(code,qty,curr_price)
                print(code,": buy",curr_price,"amount:",qty)

                self.sell(code,qty,pred_price)
                print(code,": sell",pred_price,"amount:",qty)
                self.predprices[code] = pred_price

            if time.localtime().tm_hour == 15:
                #sell all remainings
                pass
        else: print("장중 아님")
        
        print("btn",self.btn1.isChecked())
        if self.btn1.isChecked() == False:
            # self.sell_all_remainings()
            # time.sleep(10)
            self.cancel_all_buyorder()
            self.df.to_csv('./trade_record.csv',index=False)
            self.DisConnectRealData("1000")  
            self.is_exit = True
            # time.sleep(3)
            sys.exit()
            

#순서대로

    def buy(self,code,Qty,price):
        self.SendOrder(1,code,Qty,price)
        if(Qty == 0):
            Qty = "0"
        ls = [[self.get_currtime(),code,"a",price*-1,Qty]]
        df2  = pd.DataFrame(ls,columns = ['time','code','name','price','qty'])
        self.df = pd.concat([self.df,df2],ignore_index=True)
        self.df.to_csv('./trade_record.csv',index=False)

    def sell(self,code,Qty,price):
        self.SendOrder(2,code,Qty,price)
        if(Qty == 0):
            Qty = "0"
        ls = [[self.get_currtime(),code,"a",price,Qty]]
        df2  = pd.DataFrame(ls,columns = ['time','code','name','price','qty'])
        self.df = pd.concat([self.df,df2],ignore_index=True)
        self.df.to_csv('./trade_record.csv',index=False)

    def SendOrder(self, order_type, code, quantity, price):
        self.ocx.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", 
                                   ["지정가매수", "1000", self.account_no, order_type, code, quantity, price, "00", ""])

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

    def calc_rev(self,hoga_arr,price_arr):
        expec = self.predict_priceidx(price_arr)
        middle = int(len(hoga_arr)/2)
        if(expec<middle):
            return 0
        # elif middle<expec:
        elif expec*2/100 > expec-middle:
            price_arri = []
            for i in price_arr:
                price_arri.append(int(i))
            expec_price = price_arri[expec]
            middle_price = price_arri[middle]
            revenue=expec_price - middle_price
            # tax = revenue*0.0315
            tax = revenue*0.35/100
            revenue -= tax
            if(revenue>10):
                return expec_price
            else:return 0


    def get_currtime(self):
        d = str(time.localtime().tm_mon) + "/" + str(time.localtime().tm_mday) + " "
        t = str(time.localtime().tm_hour) + ":" + str(time.localtime().tm_min) +":" + str(time.localtime().tm_sec)
        t = d+t
        return t

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
        return rsult# [종목코드, [호가잔량],[호가] ]    ,

    #잔고확인함수
    # def get_account_detail(self,sPrevNext="0"):
    #     self.ocx.SetInputMultiValue(self.)

    def _receive_chejan_data(self, gubun, item_cnt, fid_list):
        print(gubun) # 1: 잔고 데이터
        # if gubun=='1':  
        code = self.get_chejan_data(9001)
        code = code[1:]
        print("code:",code,"type:",type(code))
        qty = self.get_chejan_data(933)
        self.remainamounts[code] = qty
        price = self.get_chejan_data(28)
        # print(code,".",qty,".",price)
        # hoga = self.get_each_stock_data(code)
        # print(hoga)
        # pred_price = abs(int(hoga[2][self.predict_priceidx(hoga[1])]))
        pred_price = self.predprices[code]
        if time.localtime().tm_hour != 15:
            self.sell(code,qty,pred_price)
            print(code,": sell",pred_price,"amount:",qty)
        else : 
            self.sell(code,qty,price)
            print(code,": sell",price,"amount:",qty)    
        # print("코드",self.get_chejan_data(9001))
        # print("주문가능수량",self.get_chejan_data(933))
        # print("최우선매수호가",self.get_chejan_data(28))
    def get_chejan_data(self, fid):
        ret = self.ocx.dynamicCall("GetChejanData(int)", fid)
        return ret
    

    def tr_slot(self,sScrNo,sRQName,sTrCode,sRecordName,sPrevNext):
        
        print("tr_slot")
        print(sRQName)
        # if sRQName == "예수금상세현황요청":
        #     print("예수금")
        #     deposit = self.ocx.dynamicCall(
        #         "GetCommData(QString,QString,int,QString)",sTrCode,sRQName,0,"주문가능금액"
        #     )
        #     self.budjet = int(deposit)
        #     self.ocx.account_loop.exit()
        
        # elif sRQName == "계좌평가잔고내역요청":
        #     # cnt = self.ocx.dynamicCall("GetRepeatCnt(Qstring,Qstring)",sTrCode, sRQName)
            
        #     # for i in range(cnt):
        #     #     stock_code = self.ocx.dynamicCall("GetCommData(QString,QString,int,QString)",sTrCode,sRQName,i,"종목번호")
        #     #     stock_code= stock_code.strip()[1:]

        #     #     stock+
        #     pass
        if sRQName == "실시간미체결요청":
            cnt = self.ocx.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)
            print("미체결주문수:",cnt)
            for i in range(cnt):
                stock_code = self.ocx.dynamicCall("GetCommData(QString,Qstring,int,QString)",sTrCode,sRQName,i,"종목코드")
                stock_code  = stock_code.strip()#[1:]
                # print(stock_code)

                stock_order_no = self.ocx.dynamicCall("GetCommData(QString,Qstring,int,QString)",sTrCode,sRQName,i,"주문번호")
                stock_order_no  = int(stock_order_no)
                # print("주문번호:",stock_order_no)

                stock_order_quantity = self.ocx.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "주문수량")
                stock_order_quantity = int(stock_order_quantity)

                stock_present_price = self.ocx.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "현재가")
                stock_present_price = int(
                    stock_present_price.strip().lstrip('+').lstrip('-'))

                self.ocx.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", 
                                   ["매수취소", "1000", self.account_no, 3, stock_code, stock_order_quantity, stock_present_price, "00", stock_order_no])
                print(stock_code," : ","cancel ",stock_present_price," amount: ",stock_order_quantity)
            
        
        if sRQName == "계좌평가잔고내역요청":
            cnt = self.ocx.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)
            print("잔고:",cnt)
            for i in range(cnt):
                stock_code = self.ocx.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목번호")
                stock_code = stock_code.strip()[1:]

                stock_trade_quantity = self.ocx.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "매매가능수량")
                stock_trade_quantity = int(stock_trade_quantity)

                stock_present_price = self.ocx.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "현재가")
                stock_present_price = int(stock_present_price)

                # self.sell(stock_code,stock_trade_quantity,stock_present_price)
                self.ocx.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", 
                                   ["전체매도", "1000", self.account_no, 2, stock_code, stock_trade_quantity, stock_present_price, "00", ""])
                
                # if(stock_trade_quantity == 0):
                #     Qty = "0"
                #     ls = [[self.get_currtime(),stock_code,"a",stock_present_price,Qty]]
                #     df2  = pd.DataFrame(ls,columns = ['time','code','name','price','qty'])
                #     self.df = pd.concat([self.df,df2],ignore_index=True)
                #     self.df.to_csv('./trade_record.csv',index=False)


                # stock_order_type = self.ocx.dynamicCall(
                #     "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "주문구분")
                # stock_order_type = stock_order_type.strip().lstrip('+').lstrip('-')
                # print("주문구분",stock_order_type)

            # if sPrevNext == "2":
            #     self.not_signed_account(2)
            # else:
            #     # self.cancel_screen_number(sScrNo)
            #     self.account_loop.exit()
    def cancel_all_buyorder(self,nPrevNext=0):
        print("cancel")
        self.ocx.dynamicCall("SetInputValue(QString,QString)","계좌번호",self.account_no)
        # self.ocx.dynamicCall("SetInputValue(QString,QString)","비밀번호","1702")
        # self.ocx.dynamicCall("SetInputValue(QString,QString)","비밀번호입력매체구분","00")
        # self.ocx.dynamicCall("SetInputValue(QString,QString)","조회구분","1")
        # print("미체결요청")
        self.ocx.dynamicCall("SetInputValue(QString,QString)","전체종목구분","0")
        self.ocx.dynamicCall("SetInputValue(QString,QString)","매매구분","2")#1
        self.ocx.dynamicCall("SetInputValue(QString,QString)","체결구분","1")#1
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)",
                         "실시간미체결요청", "opt10075", nPrevNext, "1000")
        # self.ocx.dynamicCall("CommRqData(QString,QString,int,QString)","실시간미체결요청","opt10075",nPrevNext,"1000")
        print("cancel complete")
        # if not self.account_loop.isRunning():
        #     self.account_loop.exec_()

    # def sell_all_remainings(self,nPrevNext=0):
    #     print("re1")
    #     self.ocx.dynamicCall("SetInputValue(QString,QString)","계좌번호",self.account_no)
    #     self.ocx.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
    #     self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)",
    #                      "계좌평가잔고내역요청", "opw00018", nPrevNext, "1000")
    #     print("re1fin")


#기타 필요한 함수들----------------
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
    
    
    # def cancel_all_buyorder(self):
    #     # self.update_stockdata()
    #     for each in self.codes:
    #         self.sell(each,self.remainamounts[each],self.buyprices[each])
    #         # self.buyprices[each] = 0
    #         # self.predprices[each]=0
    #         # self.haveamounts[each]=0
    #         # self.remainamounts[each]=0
    #     pass
    
    
    
    def __del__(self):
        # self.not_signed_account()

        self.cancel_all_buyorder()
        self.df.to_csv('./trade_record.csv',index=False)
        self.DisConnectRealData("1000")     

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()


