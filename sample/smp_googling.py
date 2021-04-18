from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

# $ pip install bs4
# $ pip install selenium
# $ pip install requests
# $ pip install pandas

baseUrl = 'https://www.google.com/search?q='
plusUrl = input('Search Keyword :')
url = baseUrl + quote_plus(plusUrl)
# 한글은 바로 사용하는 방식이 아니라, quote_plus가 변환해줌
# URL에 %CE%GD%EC 이런 거 만들어줌

# local 설치 버전 90.0.4430.72
# ChromeDriver 버전 89.0.4389.23
# driver = webdriver.Chrome('C:\Python\Study\chromedriver_win32\chromedriver.exe')
driver = webdriver.Chrome("../install/chromedriver")


driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html)

# 제목, 링크
v = soup.select('.yuRUbf')

titles = []
links = []
texts = []

for i in v:
    print(i.select_one('.LC20lb').text)  #제목
    print(i.a.attrs['href']) #링크
    title = i.select_one('.LC20lb').text
    href = i.a.attrs['href']
    titles.append(title)
    links.append(href)


data = {'title': titles, 'link': links}
data_frame = pd.DataFrame(data, columns=['title', 'link'])
data_frame.to_csv('./Googling_' + plusUrl + '.dat')


driver.close()