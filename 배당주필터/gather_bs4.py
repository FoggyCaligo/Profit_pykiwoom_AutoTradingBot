import bs4
import requests

investingCOM_url = 'https://kr.investing.com/indices/investing.com-us-500-components'


html = requests.get(investingCOM_url)
soup = bs4.BeautifulSoup(html.content,'html.parser')
table = soup.find('table',id='cr1')
body = table.find('tbody')
print(body)

