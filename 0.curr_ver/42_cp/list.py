import FinanceDataReader as fdr
import date
import input_p





price_min = int(input_p.price_min)    #최저가
price_max = int(input_p.price_max)   #최고가
vol_max = float(input_p.vol_max)#%      #가격변동률 상한 마지노선
vol_min = float(input_p.vol_min)#%       #가격변동률 하한 마지노선
search_stockamount = int(input_p.search_stockamount)#리스트 뽑을 종목 수(시가총액 상위 x개)

min_rev = float(input_p.min_rev)#%
max_rev = float(input_p.max_rev)#%
budjet = int(input_p.budjet)#예산 - 10만원
codevariable = int(input_p.codevariable)#거래할 종목 수 - 5개

print("최소가격  : ",price_min)
print("최대가격  : ",price_max)
print("최소변동률: ",vol_min)
print("최대변동률: ",vol_max)
print("추출종목수: ",search_stockamount)
print("최소수익률: ",min_rev)
print("최대수익률: ",max_rev)
print("예산     : ",budjet)
print("거래종목수: ",  codevariable)

#-------------------------------------------------------
# price_min = 5000    #최저가
# price_max = 20000   #최고가
# vol_max = 10#%      #가격변동률 상한 마지노선
# vol_min = 3#%       #가격변동률 하한 마지노선
# search_stockamount = 200 #리스트 뽑을 종목 수(시가총액 상위 x개)

# min_rev = 0.4#%
# max_rev = 50#%
# budjet = 50000#예산 - 10만원
# codevariable = 3#거래할 종목 수 - 5개
#---------------------------------------------------------------


df = fdr.StockListing("KOSPI")
df.sort_values(by=['Marcap'],ascending=False)#시가총액 큰 순서대로 정렬
top = df[:search_stockamount] #시가총액 상위 search_stockamount개 뽑기


date7 = date.get_7date()

def getls2():
    ls = []
    for each in top['Code']:
        curr_price = int(fdr.DataReader(each,date7[0])['Open'].iloc[0])
        
        if(curr_price<price_min) or (price_max<curr_price):#가격이 맞지 않으면
            continue#건너뛰기
       
        #최근 7일간 가장 낮은 가격과 가장 높은 가격 구하기
        pricearr = []
        for day in date7:
            pricearr.append(int(fdr.DataReader(each,day)['Close'].iloc[0]))
        pricearr.sort()
        min = pricearr[0]
        max = pricearr[len(pricearr)-1]

        #최저가와 최고가 사이의 변동값이 지정값보다 크면
        if (max-min)<(min*(vol_min/100)) or (max-min)>(min*vol_max/100):
            continue#넘기기
        print(" ",each, " ", curr_price)
        ls.append(each)#아니면 ls에 추가
    print("refining complete")
    return ls



#print(getls2())

