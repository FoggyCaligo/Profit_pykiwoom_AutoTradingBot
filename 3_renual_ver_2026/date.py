import datetime

def get_7date():
    answer = []
    today_date = datetime.datetime.now()
    
    for i in range(7):
        today_date = nearest_opendate(today_date)    
        answer.append(today_date.strftime("%Y-%m-%d"))
        today_date -= datetime.timedelta(days=1)
    return answer

def nearest_opendate(date):#주말 제외한 가장 가까운 영업일 찾아서 반환 (공휴일 제외는 아직 구현 안됨)
    if date.weekday()==6:#일요일이면
        return date-datetime.timedelta(days=2)#2일 빼서 반환
    elif date.weekday()==5:#토요일이면
        return date-datetime.timedelta(days=1)#1일 빼서 반환
    else:
        return date
    
print(get_7date())
print(nearest_opendate(datetime.datetime.now()))

