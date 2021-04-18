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

# 구글링 제목, 링크, 요약내용
titles = []
links = []
contents = []

for page in range(3,10):
    html = driver.page_source
    soup = BeautifulSoup(html)
    v = soup.select('.tF2Cxc')
    print(page)
    for i in v:
        v2 = i.select('.yuRUbf')
        for i2 in v2:
            title = i2.select_one('.LC20lb').text   # 제목
            title2 = title.replace(",", " ")
            href = i2.a.attrs['href']   # 링크
            print(title2)
            print(href)
            titles.append(title2)
            links.append(href)

        v3 = i.select('.IsZvec')
        for i3 in v3:
            content = i3.select_one('.aCOpRe').text     # 요약내용
            content2 = content.replace(",", " ")
            print(content2)
            contents.append(content2)

    ## 다음 페이지 클릭
    driver.find_element_by_xpath('//*[@id="xjs"]/table/tbody/tr/td[%s]/a' % page).click()

data = {'title': titles, 'link': links, 'content': contents}
data_frame = pd.DataFrame(data, columns=['title', 'link', 'content'])
data_frame.to_csv('./Googling_' + plusUrl + '.dat')

driver.close()