from pykiwoom.kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)






df = kiwoom.block_request('opt10004',
                          종목코드='005930',
                          output='주식호가요청',
                          next=0)
# print(df)

# print(['주식호가'])

for each in df:
    print(each)



