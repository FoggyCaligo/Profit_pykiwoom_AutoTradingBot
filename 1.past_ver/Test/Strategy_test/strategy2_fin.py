amount = [300,50,50,50,10,20,300,200,70,100,150,20,30,5,30,150,70,90,80,50]

amount = [50,50,50,50,50,50,50,50,50,100,50,50,50,50,50,50,50,50,50,50]


middle = int(len(amount)/2)
print("middle:",middle)

buyidx = middle
sellidx = middle+1

while(True):
    if(buyidx==0):
        break
    elif sellidx==len(amount):
        break




    if(amount[buyidx]>amount[sellidx]):
        amount[buyidx]-=amount[sellidx]
        sellidx+=1
    elif(amount[buyidx]<amount[sellidx]):
        amount[sellidx]-=amount[buyidx]
        buyidx-=1
    else:
        buyidx-=1
        sellidx+=1
    print(buyidx," ",sellidx)


sellidx+buyidx/2


rsult = int((sellidx+buyidx)/2)
print(rsult)



if(rsult<=middle):
    print("skip")
    print(0)#return 0

elif(rsult>middle):
    print("buy")
    #print(price[rsult])#return amount[rsult] : 예상가
    