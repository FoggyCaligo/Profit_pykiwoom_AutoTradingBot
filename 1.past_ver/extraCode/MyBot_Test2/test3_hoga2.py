import sys 
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import datetime

from pykiwoom.kiwoom import *



class code_realdata:
    code = "005930"
    def __init__(self,code):
        self.code = code

        #connnecct    
        kiwoom=Kiwoom()
        kiwoom.CommConnect(block=True)
        state = kiwoom.GetConnectState()
        if(state==0):
            print("연결안됨")
        elif state==1:
            print("연결완료")

        


                