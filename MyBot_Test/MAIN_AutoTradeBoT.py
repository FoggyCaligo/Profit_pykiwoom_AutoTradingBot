







from Basic_Functions import Functions as funcs
#최근 2년간의 하루단위 종가를 배열로 불러오는 함수
arr = funcs.getPriceData(0) #arr에 종가배열 저장됨

for i in range(200):#코스피200 종목 순서대로 순회
    each = funcs.get_PriceData(i)#일단위 종가 과거기록 가져오기
    
    
