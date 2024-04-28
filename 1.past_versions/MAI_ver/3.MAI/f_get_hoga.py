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
        # self.setGeometry(300, 300, 300, 400)
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.connect)
        self.ocx.OnReceiveRealData.connect(self._handler_real_data)
        # 2초 후에 로그인 진행
        QTimer.singleShot(1000 * 2, self.CommmConnect)
        self.code = code
        self.buyamount=[]
        self.buyprice=[]
        self.sellamount=[]
        self.sellprice=[]

    def connect(self):
        self.SetRealReg("1000", self.code, "41", 0)

    def CommmConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        self.statusBar().showMessage("login 중 ...")



    def _handler_real_data(self, code, real_type, data):
        self.buyamount.clear()
        self.buyprice.clear()
        self.sellamount.clear()
        self.sellprice.clear()
        
        for i in range(10):
            self.buyamount.append(self.GetCommRealData(code,71+i))
            self.buyprice.append(self.GetCommRealData(code,51+i))
            self.sellamount.append(self.GetCommRealData(code,61+i))
            self.sellprice.append(self.GetCommRealData(code,41+i))
        
        print("--------------------------")
        print(self.buyprice)
        print(self.buyamount)
        print("\n")
        print(self.sellprice)
        print(self.sellamount)
        # for i in code:
        #     print("code1",i)
        #     temp = StockClass.StockData(i,[],[],[],[])
        #     for a in range(10):
        #         temp.sellamount.append(self.GetCommRealData(i,41+a))
        #         temp.sellprice.append( self.GetCommRealData(i, 61+a))
        #         temp.buyamount.append(self.GetCommRealData(i,51+a))
        #         temp.buyprice.append(self.GetCommRealData(i, 71+a))
        #     self.stockls.append(temp)
        # print(self.stockls)
        # print("\n\n")



        # print(self.GetCommRealData(code,49))#매도9주가
        # print(self.GetCommRealData(code,69))#매도9잔량
        # print(self.GetCommRealData(code,48))#매도8주가
        # print(self.GetCommRealData(code,68))#매도8잔량
        # print(self.GetCommRealData(code,47))#매도7주가
        # print(self.GetCommRealData(code,67))#매도7잔량
        # print(self.GetCommRealData(code,46))#매도6주가
        # print(self.GetCommRealData(code,66))#매도6잔량
        # print(self.GetCommRealData(code,45))#매도5주가
        # print(self.GetCommRealData(code,65))#매도5잔량
        # print(self.GetCommRealData(code,44))#매도4주가
        # print(self.GetCommRealData(code,64))#매도4잔량
        # print(self.GetCommRealData(code,43))#매도3주가
        # print(self.GetCommRealData(code,63))#매도3잔량
        # print(self.GetCommRealData(code,42))#매도2주가
        # print(self.GetCommRealData(code,62))#매도2잔량
        # print(self.GetCommRealData(code,41))#매도1주가
        # print(self.GetCommRealData(code,61))#매도1잔량
        # print("_____________________________________")        
        # print(self.GetCommRealData(code,51))#매수1주가
        # print(self.GetCommRealData(code,71))#매수1잔량
        # print(self.GetCommRealData(code,52))#매수2주가
        # print(self.GetCommRealData(code,72))#매수2잔량
        # print(self.GetCommRealData(code,53))#매수3주가
        # print(self.GetCommRealData(code,73))#매수3잔량
        # print(self.GetCommRealData(code,54))#매수4주가
        # print(self.GetCommRealData(code,74))#매수4잔량
        # print(self.GetCommRealData(code,51))#매수1주가
        # print(self.GetCommRealData(code,71))#매수1잔량
        # print(self.GetCommRealData(code,52))#매수2주가
        # print(self.GetCommRealData(code,72))#매수2잔량
        # print(self.GetCommRealData(code,53))#매수3주가
        # print(self.GetCommRealData(code,73))#매수3잔량
        # print(self.GetCommRealData(code,54))#매수4주가
        # print(self.GetCommRealData(code,74))#매수4잔량



        

        # if real_type == "주식호가잔량":
        #     hoga_time =  self.GetCommRealData(code, 21)         
        #     ask01_price =  self.GetCommRealData(code, 41)         
        #     ask01_volume =  self.GetCommRealData(code, 61)         
        #     bid01_price =  self.GetCommRealData(code, 51)         
        #     bid01_volume =  self.GetCommRealData(code, 71)         
        #     print(hoga_time)
        #     print(f"매도호가: {ask01_price} - {ask01_volume}")
        #     print(f"매수호가: {bid01_price} - {bid01_volume}")

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
    app.exec_()#
    
    # codearr = getls.getList()
    # dataarr = []
    # for each in codearr:
    #     dataarr.append(Hoga(each))
    #     pass

    # app.exec_()


apparr = []
stockarr = getls.getList()
for each in stockarr:
    app = QApplication(sys.argv)
    window=Hoga(each)
    window.show()
    app.exec_()

