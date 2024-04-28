import datetime

#
today_date = datetime.datetime.now()
today = today_date.strftime("%Y-%m-%d")



pastdate_arr = []
temp_date = today_date
for i in range(7):
    temp_date -= datetime.timedelta(days=1)
    if(temp_date.weekday()==0):
        temp_date -= datetime.timedelta(days=2)
    pastdate_arr.append(temp_date.strftime("%Y-%m-%d"))




def get_7date():
    answer = []
    today_date = datetime.datetime.now()
    
    for i in range(7):
        today_date = nearest_opendate(today_date)    
        answer.append(today_date.strftime("%Y-%m-%d"))
        today_date -= datetime.timedelta(days=1)
    return answer



def nearest_opendate(date):#주말 제외한 가장 가까운 영업일 찾아서 반환
    if date.weekday()==6:#일요일이면
        return date-datetime.timedelta(days=2)#2일 빼서 반환
    elif date.weekday()==5:#토요일이면
        return date-datetime.timedelta(days=1)#1일 빼서 반환
    else:
        return date
    


print(get_7date())