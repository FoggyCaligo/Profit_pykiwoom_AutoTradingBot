import pandas as pd

m_rev_percent = 3
m_rev = 0
prop = 1000000
year = 6#2030
monthly_input = 200000
d = []
arr1 = ['월   ', '수익금','초기자산'+str(prop),'수익률 월 3% 가정' ]
d.append(arr1)

print(50000 * (5/100))


for y in range(year):
    
    for m in range(12):
        m_rev = prop*(3/100)
        prop+=m_rev
        arr = [str(m+1)+'월  ', '월수익금'+str(m_rev), "총자산"+str(prop), "월 저축액"+str(monthly_input) ]
        
        prop += monthly_input
        d.append(arr)
    

    arr = [str(y+1)+"년차---------------","----------","----------"]
    d.append(arr)




df = pd.DataFrame(d)
df.to_csv('./test.csv',index=False)




