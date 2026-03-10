from pykiwoom import *

km = KiwoomManager()
km.put_method(('GetMasterCodeName',"005930"))
data = km.get_method()
print(data)


tr_cmd = {
        'rqname': "opt10001",
        'trcode': 'opt10001',
        'next': '0',
        'screen': '1000',
        'input': {
            "종목코드": "005930"
        },
        'output': ['종목코드', '종목명', 'PER', 'PBR']
}

km.put_tr(tr_cmd)
data = km.get_tr()
print(data)