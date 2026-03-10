import pandas as pd
import time


def get_currtime():
    d = str(time.localtime().tm_mon) + "/" + str(time.localtime().tm_mday) + "."
    t = str(time.localtime().tm_hour) + ":" + str(time.localtime().tm_min) +":" + str(time.localtime().tm_sec)
    t = d+t
    return t




ls = [[get_currtime(),1,"a",2,3]]
df = pd.DataFrame(ls)
df.columns = ['time','code','name','price','qty']

df.to_csv("./trade_record.csv",index=False)

# df.to_csv('./trade_record.csv')

