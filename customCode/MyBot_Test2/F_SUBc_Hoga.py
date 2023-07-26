from pykiwoom.kiwoom import *




kiwoom=Kiwoom()
kiwoom.CommConnect(block=True)
state = kiwoom.GetConnectState()
account = kiwoom.GetLoginInfo("ACCNO")[1]#내 계좌 중 2번째 계좌  불러오기
if(state==0):
    print("연결안됨")
elif state==1:
    print("연결완료")


# df_single = kiwoom.block_request('opt10004','005930','호가',0)


# code = '005930'
# kiwoom.SetInputValue("code",code)
# kiwoom.CommRqData("호가조회","opt10004",0,'0000')

# print(df_single)


print(kiwoom.GetCommData('OPT00001', '주식기본정보', 0, '현재가'))

print()



strRealData = kiwoom.GetCommRealData('005930;060310', 10); 


kiwoom.GetCommRealData('005930',10)
print(kiwoom.OnReceiveRealData('10004',10,"전문"))



# print(kiwoom.GetOutputValue)