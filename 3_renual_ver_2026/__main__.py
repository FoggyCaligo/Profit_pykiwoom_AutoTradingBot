from PyQt5 import QtWidgets
import sys

import data.params
import api.client
import data.stock_list
import data.record

from PyQt5.QAxContainer import QAxWidget
w = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
print("null?", w.isNull())             # True 면 컨트롤을 못 찾은 것
print("avail signals:", [m.name() for m in w.metaObject().methodCount()])


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)      # ← 반드시 먼저
    apiClass = api.client.API()                 # 이제 QAxWidget이 정상화
    paramsClass = data.params.Params()
    stockListClass = data.stock_list.StockList(apiClass, paramsClass)
    print(stockListClass.stockList)

