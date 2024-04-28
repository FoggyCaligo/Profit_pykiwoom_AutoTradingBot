import f_order as order
import f_logic as logic

class StockManager:
    def __init__(self,code):
        self.code = code
        # self.buyprice = 0
        self.predprice = 0
        self.haveamount = 0

        self.hoga_arr = []
        self.price_arr = []

        self.budjet = 0


    def buy(self,price_arr,hoga_arr):
        if self.haveamount == 0:
            if(self.calc_rev(hoga_arr,price_arr)) != 0:
                curr_price = self.price_arr[int(len(self.hoga_arr)/2)]
                self.haveamount = self.budjet/10/curr_price
                order.buy(self.code,self.haveamount,curr_price)
                self.predprice =curr_price
                
            pass

    def sell(self,price_arr,hoga_arr):
        self.price_arr=price_arr
        self.hoga_arr = hoga_arr
        if self.haveamount != 0:
            curr_price = self.price_arr[int(len(self.hoga_arr)/2)]
            if curr_price >= self.predprice:
                order.sell(self.code,self.haveamount,curr_price)
            
        pass

    def predict_priceidx(self,hoga_arr):
        self.hoga_arr = hoga_arr
        middle = int(len(self.hoga_arr)/2)
        buyidx = middle
        sellidx = middle+1
        while(True):
            if(buyidx==0):break
            elif sellidx==len(self.hoga_arr):break
            if(self.hoga_arr[buyidx > self.hoga_arr[sellidx]]):
                self.hoga_arr[buyidx]-=self.hoga_arr[sellidx]
                sellidx+=1
            elif(self.hoga_arr[buyidx]<self.hoga_arr[sellidx]):
                self.hoga_arr[sellidx]-=self.hoga_arr[buyidx]
                buyidx-=1
            else:
                buyidx-=1
                sellidx+=1
        rsult = int((sellidx+buyidx)/2)
        return rsult

    def calc_rev(self,hoga_arr,price_arr):
        self.price_arr = price_arr
        self.hoga_arr = hoga_arr
        expec = self.predict_priceidx(self.price_arr)
        middle = int(len(self.hoga_arr)/2)
        if(expec<middle):
            return 0
        elif middle<expec:
            expec_price = price_arr[expec]
            middle_price = price_arr[middle]
            revenue=expec_price - middle_price
            tax = revenue*0.0315
            revenue -= tax
            if(revenue>10):
                return expec_price
            else:return 0
    def get_code(self):
        return self.code