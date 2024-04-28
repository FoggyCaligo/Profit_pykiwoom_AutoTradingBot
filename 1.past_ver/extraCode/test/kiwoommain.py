import sys
from PyQt5.QtWidgets import *
from pykiwoom.kiwoom import *
from config import *

class KiwoomMain:
    def __init__(self):
        self.kiwoom=Kiwoom()
        self.kiwoom.CommConnect()

    def OPT10004(self,code):
        self.kiwoom.output_list = output_list['OPT10004']

        self.kiwoom.SetInputValue("종목코드", code)
        return self.kiwoom.CommRqData("OPT10004", "OPT10004", 0, "0101")

        return self.kiwoom.ret_data['OPT10004']
    

app = QApplication(sys.argv)
api_con = KiwoomMain()

result = api_con.OPT10004("005930")
print(result)