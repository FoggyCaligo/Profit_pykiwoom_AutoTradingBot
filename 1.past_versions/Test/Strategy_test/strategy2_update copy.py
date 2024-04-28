amount = [500,50,50,50,50,50,50,200,70,100,50,50,50,50,50,50,50,50,50,50]

middle = int(len(amount)/2)
print("middle:",middle)

buyidx = middle-1
sellidx = middle

while(True):
    if(buyidx==0):
        break
    if sellidx==len(amount):
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
    print(sellidx," ",buyidx)


rsult = int((sellidx-middle + middle-buyidx)/2)
print(rsult)
    