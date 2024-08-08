from pykiwoom.kiwoom import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import list
import time
import datetime


import csvRecord
import hogaRecord

class Kiwoom(QMainWindow):
    def __init__(self):
        super().__init__()

        #추출된 종목 리스트 받아오기
        self.codes = list.getls2()

        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.connect)#정제된 종목리스트의 종목들 구독하기
        self.ocx.OnReceiveRealData.connect(self._handler_real_data)#실시간 데이터를 받을 때마다 self._hander_real_data를 작동시키도록 등록
        
        self.ocx.OnReceiveChejanData.connect(self.receive_chajandata)        


        # 2초 후에 로그인 진행
        QTimer.singleShot(100 * 2, self.CommmConnect)
        
        #self.account_no =  "8082751111"#모의투자계좌
        self.account_no = "5704609010" #실계좌
        self.data_ls = {}
        self.remain_dict = {}

        self.hogarecord = hogaRecord.hogaRecord()
        self.isbuy = True
        self.endbuy = False

    #실제 거래 진행 알고리즘
    def _handler_real_data(self,code,real_type,data):#루프 반복되는 함수 -> 한번 호출당 종목 하나
        #호가 데이터 기록
        hoga = self.get_each_hoga_data(code)
        self.hogarecord.record(code,hoga)

        #9시반 ~ 12시 : 정상거래시간
        #if now<=target1:#=========================================
            #예상가 계산해서 쌓아두기
            #ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        if real_type=="주식호가잔량":
                pred = self.get_pred(code)#호가 변한 정보가 받아와지면 해당 종목의 예상가 얻어오기
                #2024.7/27 추가. 오류 시 삭제 요망.
                # if pred[-1]<list.min_rev or list.max_rev<pred[-1]:#수익률이 마지노선 이하거나, 이상하게 높으면
                #     del self.data_ls[code]#리스트에서 해당 종목 지우기
                #2024/7/27ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
                #print(code, " " , pred)
                self.data_ls[code] = pred#일단 예상가 전부 저장


            #다 쌓이면 수익률 상위(self.codevariable)의 종목들 거래.
            #ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        if len(self.data_ls) == len(self.codes) and self.isbuy and self.endbuy==False:#dict 꽉 차면(& 이미 산게 아니면)-> ls로 받아온 정제리스트 안의 모든 종목들의 수익률이 계산되어 저장된 경우
                
                self.dls = sorted(self.data_ls.items(), key=lambda x: x[1][3], reverse=True)#수익률 높은 순서대로 정렬
                
                print("final refined tradable stock lists ")
                print("\n\n\n")
                for each in self.dls:
                    print(each)
                print("\n\n\n")

                money_per_code = list.budjet/list.codevariable#거래할 종목 수만큼 예산을 분할
    
                for i in range(list.codevariable):#자동거래(매수) -> 수익률 높은 순으로 정렬된 리스트에서 상위(거래할종목수)개의 종목 거래
                    print("buy",self.dls[i][1][3])
                    if self.dls[i][1][3] < 0.315:#수수료+세금 비율보다 수익률이 더 작으면:
                        print("not suitable.",self.dls[i][1][3])
                        continue#건너뛰기
                    qty = money_per_code/self.dls[i][1][1]#종목당 할당된 예산만큼 수량을 결정
                    self.buy(self.dls[i][0], qty, self.dls[i][1][1])#수익률 계산할 당시의 현재가로 매수  
                    time.sleep(0.5)
                
                for i in range(list.codevariable):#자동거래(매도)  위의 if문과 같음
                    print("sell",self.dls[i][1][3])
                    if self.dls[i][1][3] < 0.315:#수수료+세금 비율보다 수익률이 더 작으면:
                        print("not suitable.",self.dls[i][1][3])
                        continue#건너뛰기
                    qty = money_per_code/self.dls[i][1][1]  #위와 같음                  
                    self.sell(self.dls[i][0], qty, self.dls[i][1][2])#순서 뒤집으면 매도 되는지 확인해보기
                    time.sleep(0.5)            
                
                time.sleep(1)         
                self.isbuy=False
                #csvRecord.csv.onExit()
                
        #12시 ~ 1시 : 매도시간
        #1시~3시 : 땡처리(매수가로 판매)
        #elif now<=targetend:#=========================================
            
            #pass
        #3시 이후 : 현재가 매도.
        #elif now>=targetend:
            
            #pass


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
        #상장폐지 종목일경우
        # if '0' in hoga[2] or '-0' in hoga[2] or 0 in hoga[2]:
        #     print("Error. 0 in hoga.")
        #     return 0
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



    #체결정보 받아오는 함수들
    def receive_chajandata(self,sGubun,nItemCnt,sFidList):
        
        #12시 이후면 매수 종료
        now = datetime.datetime.now()
        now = now.time()
        target = now.replace(hour=12,minute=0)
        if now>=target:
            self.endbuy=True
        #3시 이후면 프로그램 종료
        target2 = now.replace(hour=15,minute=0)
        if now>= target2:
            end_trade()
        
        
        if sGubun=='0':#체결, 접수 등의 데이터
            
            code = self.__getchejandata('9001').strip()
            name = self.__getchejandata('302').strip()
            bs = self.__getchejandata('905').strip()
            price = self.__getchejandata('910').strip()
            qty = self.__getchejandata('911').strip()
            susuryo = self.__getchejandata('938').strip()
            tax = self.__getchejandata('939').strip()
            
            remain = self.__getchejandata('902').strip()
            state = self.__getchejandata('902').strip()
            
            code = code[1:]
            if qty!=" " and qty!="":    
                if '+매수' in bs:
                    self.remain_dict[code] = int(qty)
                    #거래기록
                    csvRecord.csv.add_b(name,code,price,qty,(tax),(susuryo))
                elif '-매도' in bs:
                    #거래기록
                    csvRecord.csv.add_s(name,code,price,qty,(tax),(susuryo))
                    #매도된 만큼 빼기
                    self.remain_dict[code] -= int(qty)
                    #잔량이 0인 종목 제거 
                    if self.remain_dict[code]==0:
                        del self.remain_dict[code]
                    #종목딕셔너리에 값이 모두 빠졌으면
                    if len(self.remain_dict)==0:
                        self.data_ls = {}
                    self.isbuy=True#재매수
                    #전부 매도 시:
                
                print("체결:",code,name,bs,price,qty,susuryo,tax,state)
                


    def __getchejandata(self,fid):
        return self.ocx.dynamicCall("GetChejanData(int)",fid)
    
    def __del__(self):
        csvRecord.csv.onExit()



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
    h = time.localtime().tm_hour
    m = time.localtime().tm_min    
    now = datetime.datetime.now()
    now = now.time()
    target = now.replace(hour=9,minute=30)

    while(now<=target):   
        now = datetime.datetime.now()
        now = now.time()
    print("loop out")

    window = Kiwoom()
    window.show()
    app.exec_()
    
def end_trade(): 
    app.quit()  
    #sys.exit(app.exec_())



#프로그램 작동 시 바로 작동되도록.
start_trade()

