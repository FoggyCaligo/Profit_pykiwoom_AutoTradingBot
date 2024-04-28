from pykiwoom.kiwoom import *

kiwoom=Kiwoom()
kiwoom.CommConnect(block=True)

account_num = kiwoom.GetLoginInfo("ACCOUNT_CNT") #전체 계좌 수
accounts=kiwoom.GetLoginInfo("ACCNO")#전체 계좌 리스트

user_id = kiwoom.GetLoginInfo("USER_ID")
user_name = kiwoom.GetLoginInfo("USER_NAME")
keyboard = kiwoom.GetLoginInfo("KEY_BSECGB")#키보드보안 해지여부
firewall = kiwoom.GetLoginInfo("FIREW_SECGB")

print(account_num)
print(accounts)
print(user_id)
print(user_name)
print(keyboard)
print(firewall)


