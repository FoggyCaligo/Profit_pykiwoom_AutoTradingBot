import pandas as pd
import time

class csvRecord:
    def __init__(self):
        self.df = pd.read_csv("trade_record2.csv")
    def get_currtime(self):

        d = str(time.localtime().tm_year)+'.'+str(time.localtime().tm_mon) + "/" + str(time.localtime().tm_mday) + " "
        t = str(time.localtime().tm_hour) + ":" + str(time.localtime().tm_min) +":" + str(time.localtime().tm_sec)
        t = d+t
        return t


    def add(self,code,type,price,qty):
        ls = [self.get_currtime(),'/'+code,type,price,qty]
        temp = pd.DataFrame([ls],columns = ['time','code','type','price','qty'])
        self.df = pd.concat([self.df, temp],ignore_index=True)
        
    def onExit(self):#마지막 종료 시
        self.df.to_csv('./trade_record2.csv',index=False)#self.df를 csv에 저장




csv = csvRecord()

# csv.add("005930","Buy ","70000",1)
# csv.add("005930","Sell","70000",2)
# csv.onExit()