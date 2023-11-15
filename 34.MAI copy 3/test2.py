from tkinter.tix import COLUMN
import pandas as pd
import time


def get_currtime():
    d = str(time.localtime().tm_mon) + "/" + str(time.localtime().tm_mday) + "."
    t = str(time.localtime().tm_hour) + ":" + str(time.localtime().tm_min) +":" + str(time.localtime().tm_sec)
    t = d+t
    return t



df = pd.read_csv("trade_record.csv")
# df.columns = ['time','code','name','price','qty']

ls2 = [[get_currtime(),2,"b",3,4]]
df2 = pd.DataFrame(ls2,columns = ['time','code','name','price','qty'])



df = pd.concat([df,df2],ignore_index=True)

df.to_csv("./trade_record.csv",index=False)
