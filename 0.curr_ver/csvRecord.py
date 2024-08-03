import pandas as pd
import time

class csvRecord:
    def __init__(self):
        self.csvloc = "./42/trade_record3.csv"
        self.df = pd.read_csv(self.csvloc)
        self.dict = {}#종목별 매수금액 저장(매도 시 수익률 계산에 필요)
    def get_currtime(self):

        d = str(time.localtime().tm_year)+'.'+str(time.localtime().tm_mon) + "/" + str(time.localtime().tm_mday) + "."
        t = str(time.localtime().tm_hour) + ":" + str(time.localtime().tm_min) +":" + str(time.localtime().tm_sec)
        t = d+t
        return t

    def add(self,code,type,price,qty):
        ls = [self.get_currtime(),'/'+code,type,price,qty]
        temp = pd.DataFrame([ls],columns = ['time','code','type','price','qty'])
        self.df = pd.concat([self.df, temp],ignore_index=True)

    #수수료 0.015% 세금 0.2%        
    def add_b(self,code,price,qty):
        price = int(price)
        ls = [self.get_currtime(),'/'+code,"Buy.",price,qty, price*qty, 0, float(price)*0.015/100,"0","0"]
        temp = pd.DataFrame([ls],columns = ['시간','종목코드','거래타입','거래가','수량','총거래금', '세금','수수료','수익금','수익률'])
        self.df = pd.concat([self.df, temp],ignore_index=True)
        self.dict[code] = float(price)*float(qty)+float(price)*0.015/100#매수가*수량+수수료
    def add_s(self,code,price,qty):
        price = int(price)
        buy = self.dict[code]
        sell = float(price*qty) + float(price)*0.2/100 + float(price)*0.015/100
        #시간 종목코드 거래타입 거래가 수량 총거래금 세금 수수료 수익금 수익률  
        ls = [self.get_currtime(),'/'+code,"Sell",price,qty, price*qty, float(price)*0.2/100, float(price)*0.015/100,int(sell-buy),int(sell-buy)/buy*100]
        temp = pd.DataFrame([ls],columns = ['시간','종목코드','거래타입','거래가','수량','총거래금', '세금','수수료','수익금','수익률'])
        self.df = pd.concat([self.df, temp],ignore_index=True)
        


        




    def onExit(self):#마지막 종료 시
        self.df.to_csv(self.csvloc,index=False)#self.df를 csv에 저장




csv = csvRecord()
# csv.add_b("005930","70000",3)
# csv.add_s("005930","71000",3)
# csv.onExit()