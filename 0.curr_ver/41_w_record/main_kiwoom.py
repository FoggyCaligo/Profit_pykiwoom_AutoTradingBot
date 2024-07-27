from pykiwoom.kiwoom import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import list
import time

import csvRecord


class Kiwoom(QMainWindow):
    def __init__(self):
        super().__init__()

        #추출된 종목 리스트 받아오기
        self.codes = list.getls2()

        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.connect)#정제된 종목리스트의 종목들 구독하기
        self.ocx.OnReceiveRealData.connect(self._handler_real_data)#실시간 데이터를 받을 때마다 self._hander_real_data를 작동시키도록 등록
       
        # 2초 후에 로그인 진행
        QTimer.singleShot(1000 * 2, self.CommmConnect)
        
        #self.account_no = "8075724911"#모의투자계좌
        self.account_no = "5704609010" #실계좌
        
        self.min_rev = 0.4#%
        self.max_rev = 50#%

        self.budjet = 50000#예산 - 10만원
        self.codevariable = 3#거래할 종목 수 - 5개
        
        self.data_ls = {}


    #실제 거래 진행 알고리즘
    def _handler_real_data(self,code,real_type,data):#루프 반복되는 함수 -> 한번 호출당 종목 하나
        #예상가 계산해서 쌓아두기
        #ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        if real_type=="주식호가잔량":
            pred = self.get_pred(code)#호가 변한 정보가 받아와지면 해당 종목의 예상가 얻어오기
            
            #2024.7/27 추가. 오류 시 삭제 요망.
            if pred[-1]<self.min_rev or self.max_rev<pred[-1]:#수익률이 마지노선 이하거나, 이상하게 높으면
                del self.date_ls[code]#리스트에서 해당 종목 지우기
            #2024/7/27ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

            print(code, " " , pred)
            self.data_ls[code] = pred#일단 예상가 전부 저장

        #다 쌓이면 수익률 상위(self.codevariable)의 종목들 거래.
        #ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

        if len(self.data_ls) == len(self.codes):#dict 꽉 차면 -> ls로 받아온 정제리스트 안의 모든 종목들의 수익률이 계산되어 저장된 경우
            
        
            self.dls = sorted(self.data_ls.items(), key=lambda x: x[1][3], reverse=True)#수익률 높은 순서대로 정렬
            
            print("final refined tradable stock lists ")
            print("\n\n\n")
            for each in self.dls:
                print(each)
            print("\n\n\n")

            money_per_code = self.budjet/self.codevariable#거래할 종목 수만큼 예산을 분할
  
            for i in range(self.codevariable):#자동거래(매수) -> 수익률 높은 순으로 정렬된 리스트에서 상위(거래할종목수)개의 종목 거래
                print(self.dls[i])
                qty = money_per_code/self.dls[i][1][1]#종목당 할당된 예산만큼 수량을 결정
                self.buy(self.dls[i][0], qty, self.dls[i][1][1])#수익률 계산할 당시의 현재가로 매수  
                #csv로 해당 거래 기록. 2024.7/27 
                csvRecord.csv.add(self.dls[i][0],"Buy ",self.dls[i][1][1],qty)
                time.sleep(0.5)


                
            for i in range(self.codevariable):#자동거래(매도)  위의 if문과 같음
                qty = money_per_code/self.dls[i][1][1]  #위와 같음                  
                self.sell(self.dls[i][0], qty, self.dls[i][1][2])#순서 뒤집으면 매도 되는지 확인해보기
                #csv로 해당 거래 기록. 2024.7/27 
                csvRecord.csv.add(self.dls[i][0],"Sell",self.dls[i][1][2],qty)
                time.sleep(0.5)            

            time.sleep(1)            
            csvRecord.csv.onExit()
            end_trade()

    #오류 시 주석해제 요망.
    # def SendOrder(self, order_type, code, quantity, price):
    #     self.ocx.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", 
    #                                ["지정가매수", "1000", self.account_no, order_type, code, quantity, price, "00", ""])
    

    def buy(self,code,qty,price):
        self.ocx.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", 
                                   ["지정가매수", "1000", self.account_no, 1, code, qty, price, "00", ""])
    def sell(self,code,qty,price):
        self.ocx.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", 
                                   ["지정가매도", "1000", self.account_no, 2, code, qty, price, "00", ""])



    #주가 예측 핵심 알고리즘 start ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    def get_pred(self,code):#예상가 & 예상 수익률 반환
        hoga = self.get_each_hoga_data(code)#해당 종목의 호가정보를 받아옴
        #print("hoga:",hoga)#--실험해 봐야 함.
        if '0' in hoga[2] or '-0' in hoga[2] or 0 in hoga[2]:#상장폐지 종목일경우
            print("Error. 0 in hoga.")
            return
        #print("hoga:",hoga[2][int(len(hoga[1])/2)])
        curr_price = abs(int(hoga[2][int(len(hoga[1])/2)]))
        pred_price = abs(int(hoga[2][self.predict_priceidx(hoga[1])]))#예상가의 호가인덱스를 계산
        rev_per = (pred_price - curr_price) / curr_price*100#예상수익률 계산
        
        answer = [code,curr_price,pred_price, rev_per]#종목코드, 현재가, 예상가, 예상수익률 리스트에 담고
        return answer#위의 리스트 반환

    def get_each_hoga_data(self,code):#각 종목별 호가 받아오는 함수
        rsult = []
        temp_amount = []
        temp_price = []
        for i in reversed(range(10)):
            temp = self.GetCommRealData(code,71+i)
            #print("temp",temp)
            temp_amount.append(self.GetCommRealData(code,71+i))#매수호가
            temp_price.append(self.GetCommRealData(code,51+i))#매수수량
        for i in range(10):
            temp_amount.append(self.GetCommRealData(code,61+i))#매도호가
            temp_price.append(self.GetCommRealData(code,41+i))#매도수량
        rsult.append(code)
        rsult.append(temp_amount)
        rsult.append(temp_price)
        #print(rsult)
        return rsult# [종목코드, [호가잔량],[호가] ]    ,
    def predict_priceidx(self,hoga_arr):#예상가 호가 위치 인덱스 찾기
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
    #주가 예측 핵심 알고리즘 end ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ





    #기타 필요한 함수들
    def CommmConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        self.statusBar().showMessage("login 중 ...")
    def connect(self):
        strarr = ""
        for each in self.codes:#여기서 오류 안나는지 확인해보기.
            strarr += each+";"
        strarr = strarr[:-1]
        self.SetRealReg("1000",strarr, "41", 0)
    def SetRealReg(self, screen_no, code_list, fid_list, real_type):
        self.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)", 
                              screen_no, code_list, fid_list, real_type)
    
    def GetCommRealData(self, code, fid):
        data = self.ocx.dynamicCall("GetCommRealData(QString, int)", code, fid) 
        return data



app = QApplication(sys.argv)


#on/off 함수
def start_trade():
    window = Kiwoom()
    window.show()
    app.exec_()

def end_trade():
    sys.exit(app.exec_())



#프로그램 작동 시 바로 작동되도록.
start_trade()
