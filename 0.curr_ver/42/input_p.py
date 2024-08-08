import tkinter as tk  
import pandas as pd  

from tkinter import ttk








#파라미터 입력창----------------------------------------------------
csvloc = "./42/parameter.csv"
df = pd.read_csv(csvloc)
df = df.columns
print(df)
price_min = df[0]    #최저가
price_max = df[1]   #최고가
vol_max = df[2]#%      #가격변동률 상한 마지노선
vol_min = df[3]#%       #가격변동률 하한 마지노선
search_stockamount = df[4] #리스트 뽑을 종목 수(시가총액 상위 x개)

min_rev = df[5]#%
max_rev = df[6]#%
budjet = df[7]#예산 - 10만원
codevariable = df[8]#거래할 종목 수 - 5개



window = tk.Tk()
window.title="주식 자동거래 파라미터 조정용 탭"

window.resizable=(True,True)



l_price_min = tk.Label(window,text="종목 최저가")
l_price_min.grid(row=1,column=1)
i_price_min = tk.Entry(window,textvariable=str(price_min))    #최저가
i_price_min.grid(row=2,column=1)
i_price_min.insert(0,str(price_min))
l_price_max = tk.Label(window,text="종목 최고가")
l_price_max.grid(row=1,column=2)
i_price_max = tk.Entry(window,textvariable=str(price_max))   #최고가
i_price_max.grid(row=2,column=2)
i_price_max.insert(0,str(price_max))

l_vol_max = tk.Label(window,text="가격변동률 상한 마지노선(%)")
l_vol_max.grid(row=1,column=3)
i_vol_max = tk.Entry(window,textvariable=str(vol_max))#%      #가격변동률 상한 마지노선
i_vol_max.grid(row=2,column=3)
i_vol_max.insert(0,str(vol_max))

l_vol_min = tk.Label(window,text="가격변동률 하한 마지노선(%)")
l_vol_min.grid(row=1,column=4)
i_vol_min = tk.Entry(window,textvariable=str(vol_min))#%       #가격변동률 하한 마지노선
i_vol_min.grid(row=2,column=4)
i_vol_min.insert(0,str(vol_min))

l_search_stockamount = tk.Label(window,text="리스트 뽑을 종목 수(시가총액 상위 x개)")
l_search_stockamount.grid(row=1,column=5)
i_search_stockamount = tk.Entry(window,textvariable=str(search_stockamount)) #리스트 뽑을 종목 수(시가총액 상위 x개)
i_search_stockamount.grid(row=2,column=5)
i_search_stockamount.insert(0,str(search_stockamount))

l_min_rev = tk.Label(window,text = "수익률 하한(%)")
l_min_rev.grid(row=1,column=6)
i_min_rev = tk.Entry(window,textvariable=str(min_rev))#%
i_min_rev.grid(row=2,column=6)
i_min_rev.insert(0,str(min_rev))

l_max_rev = tk.Label(window,text = "수익률 상한(%)")
l_max_rev.grid(row=1,column=7)
i_max_rev = tk.Entry(window,textvariable=str(max_rev))
i_max_rev.grid(row=2,column=7)
i_max_rev.insert(0,str(max_rev))

l_budjet = tk.Label(window,text="투자 가능한 예산(단위:원)")#예산 - 10만원
l_budjet.grid(row=1,column=8)
i_budjet = tk.Entry(window,textvariable=str(budjet))#예산 - 10만원
i_budjet.grid(row=2,column=8)
i_budjet.insert(0,str(budjet))

l_codevariable = tk.Label(window,text="거래할 종목 수")
l_codevariable.grid(row=1,column=9)
i_codevariable = tk.Entry(window,text="거래할 종목 수")
i_codevariable.grid(row=2,column=9)
i_codevariable.insert(0,str(codevariable))











def f_submit():
    csvloc = "./42/parameter.csv"
    df = pd.read_csv(csvloc)
    dfi = pd.DataFrame()
    print(df)

    if i_price_min.get() is not None: 
        price_min=i_price_min.get()
        dfi.loc[0,0] = price_min
    else: price_min = dfi.loc[0,0]
    if i_price_max.get() is not None: 
        price_max=i_price_max.get()
        dfi.loc[0,1] = price_max
    else: price_max = dfi.loc[0,1]
    
    if i_vol_max.get() is not None: 
        vol_max=i_vol_max.get()
        dfi.loc[0,2] = vol_max
    else: vol_max = dfi.loc[0,2]
    if i_vol_min.get() is not None: 
        vol_min=i_vol_min.get()
        dfi.loc[0,3] = vol_min
    else: vol_min = dfi.loc[0,3]
    
    if i_search_stockamount.get() is not None: 
        search_stockamount=i_search_stockamount.get()
        dfi.loc[0,4] = search_stockamount
    else: search_stockamount = dfi.loc[0,4]

    
    if i_min_rev.get() is not None: 
        min_rev=i_min_rev.get()
        dfi.loc[0,5] = min_rev
    else: min_rev = dfi.loc[0,5]
    if i_max_rev.get() is not None: 
        max_rev=i_max_rev.get()
        dfi.loc[0,6] = max_rev
    else: max_rev = dfi.loc[0,6]

    if i_budjet.get() is not None: 
        budjet=i_budjet.get()
        dfi.loc[0,7] = budjet
    else: budjet = dfi.loc[0,7]

    if i_codevariable.get() is not None: 
        codevariable=i_codevariable.get()
        dfi.loc[0,8] = codevariable
    else: codevariable = dfi.loc[0,8]

    

    print("최소가격  : ",price_min)
    print("최대가격  : ",price_max)
    print("최소변동률: ",vol_min)
    print("최대변동률: ",vol_max)
    print("추출종목수: ",search_stockamount)
    print("최소수익률: ",min_rev)
    print("최대수익률: ",max_rev)
    print("예산     : ",budjet)
    print("거래종목수: ",  codevariable)

    print(dfi)
    empty = pd.DataFrame()
    empty.to_csv(csvloc,mode='w')#self.df를 csv에 저장
    dfi.to_csv(csvloc,index=False,header=False)#self.df를 csv에 저장


    
print("최소가격  : ",price_min)
print("최대가격  : ",price_max)
print("최소변동률: ",vol_min)
print("최대변동률: ",vol_max)
print("추출종목수: ",search_stockamount)
print("최소수익률: ",min_rev)
print("최대수익률: ",max_rev)
print("예산     : ",budjet)
print("거래종목수: ",  codevariable)



submit = tk.Button(window, text="submit",command=f_submit)
submit.grid(row=2,column=10)   



#이전 거래기록 불러오는 곳
record_csvloc = "./42/trade_record3.csv"
record = pd.read_csv(record_csvloc)

table = ttk.Treeview(window, columns=('시간','종목코드','거래타입','거래가','수량','총거래금', '세금','수수료','수익금','수익률'))
table.grid(row=3,column=1,columnspan=10)

table.heading("시간",text="시간")
table.heading("종목코드",text="종목코드")
table.heading("거래타입",text="거래타입")
table.heading("거래가",text="거래가")
table.heading("수량",text="수량")
table.heading("총거래금",text="총거래금")
table.heading("세금",text="세금")
table.heading("수수료",text="수수료")
table.heading("수익금",text="수익금")
table.heading("수익률",text="수익률")

table.column("시간",width=150)
table.column("종목코드",width=60)
table.column("거래타입",width=60)
table.column("거래가",width=100)
table.column("수량",width=100)
table.column("총거래금",width=100)
table.column("세금",width=100)
table.column("수수료",width=100)
table.column("수익금",width=100)
table.column("수익률",width=100)


print('\n\n')
print(record)
for i in range(len(record)):
    print("------")
    print(record.loc[i].values)
    table.insert("","end",text="",values=record.loc[i].values)
    





window.mainloop()









        