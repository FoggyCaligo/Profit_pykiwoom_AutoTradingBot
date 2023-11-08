import time

now = time

print("시 : ", now.localtime().tm_hour)

if now.localtime().tm_hour == 16:
    print("오후 4시")