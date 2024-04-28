


amount = [300,50,50,50,10,20,300,200,70,100,
          150,20,30,5,30,150,70,90,80,50]
amount = [300,50,50,50,10,20,300,200,70,100,150,20,30,5,30,150,70,90,80,50]
amount = [50,50,50,50,50,50,50,50,50,100,
          50,50,50,50,50,50,50,50,50,50]
price  = [10000,20000,30000,40000,50000,60000,70000,80000,90000,101000,110000,120000,130000,140000,150000,160000,170000,180000,190000,200000]



assumePrice = 0
assumePriceIndex = 10



def calc_assumePriceIndex(amount_arr):
    middle = int(len(amount_arr)/2)
    buyidx = middle
    sellidx = middle+1
    while(True):
        if(buyidx==0):break
        elif sellidx==len(amount_arr):break
        if(amount_arr[buyidx]>amount_arr[sellidx]):
            amount_arr[buyidx]-=amount_arr[sellidx]
            sellidx+=1
        elif(amount_arr[buyidx]<amount_arr[sellidx]):
            amount_arr[sellidx]-=amount_arr[buyidx]
            buyidx-=1
        else:
            buyidx-=1
            sellidx+=1

    rsult = int((sellidx+buyidx)/2)
    return rsult#예상가:hoga_pricearr[rsult], 중간값: int(len(hoga_arr)/2)


def decision(amount_arr,price_arr):
    expec = calc_assumePriceIndex(amount_arr)
    middle = int(len(amount_arr)/2)
    middle = 10
    if expec<middle:
        return 0
    
    if(middle<expec):
        expec_price = price_arr[expec]
        middle_price = price_arr[middle]
        revenue = expec_price-middle_price
        tax = revenue*0.00315
        print("tax:",tax)
        revenue -=tax
        print("revenue:",revenue)
        if(revenue>10):
            return expec_price
        else: return 0

