import pandas as pd
import time

class hogaRecord:
    def __init__(self):
        self.df = pd.DataFrame()
        self.loc = "42/past_data/"

    def record(self,code,hoga):
        hoga.insert(0,code)
        hoga.insert(0,self.get_currtime())
        #print(hoga)
        temp = pd.DataFrame([hoga])
        self.df = pd.concat([self.df,temp],ignore_index=True)
        #print(self.df)
        pass

    def get_currtime(self):        
        d = str(time.localtime().tm_year)+'_'+str(time.localtime().tm_mon) + "_" + str(time.localtime().tm_mday) + "]"
        t = str(time.localtime().tm_hour) + "]" + str(time.localtime().tm_min) +"]" + str(time.localtime().tm_sec)
        t = d+t
        return t


    def __del__(self):
        self.df.to_csv(self.loc+self.get_currtime()+'.csv',index=False)




# hoga = hogaRecord()
# hoga.record('005940',[1,2,3,4,5,6,7,8,9,10])
# del hoga