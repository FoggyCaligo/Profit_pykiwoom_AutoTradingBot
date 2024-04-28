import pandas as pd

base = 200000#초기 자본금
reve_perc = 4#배당 수익률
grow_perc = 6#배당 성장률

price = 10000#주가
qty = base/price#수량
y_reve = reve_perc*price/100*qty#연간배당금
m_reve = y_reve/12#월당배당금


t = ['초기자본금','배당수익률','배당성장률','주가','수량','시작 연배당금','시작 월배당금']
value = [base,reve_perc,grow_perc,price,qty,y_reve,m_reve]
title = pd.DataFrame()
title['비고'] = t
title['값'] = value
title.transpose()
print(title)


year = 15#계산년수




df = pd.DataFrame()
base1 = base
grow_reve = 0
qty1 = qty
y_reve1 = y_reve
m_reve1 = m_reve


df = pd.DataFrame()
df['0'] = ['년수','자본금','수량','성장배당','연배당금','월배당금']

for i in range(year):
    #0년수,1자본금,2수량,3성장배당,4연배당금,5월배당금
    base1 += y_reve1
    grow_reve = y_reve1*grow_perc/100
    y_reve1 += grow_reve
    m_reve1 += y_reve1/12
    df[str(i+1)] = [str(i+1),int(base1),int(qty),int(grow_reve),int(y_reve1),int(m_reve1)]
    

df = df.transpose()
print(df)



