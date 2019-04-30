import time
from random import randint

from bs4 import BeautifulSoup
from requests import get
from requests import Session
from urllib.parse import unquote
from urllib.parse import quote
from urllib.request import FancyURLopener
from datetime import datetime

from openpyxl import Workbook

urlList = []
write_wb = Workbook()

def chosun_aticle_list(query):
    pageCount = 1
    queryString = quote(query)
    #queryString = "%22%EB%B0%9C%EB%8B%AC%EC%9E%A5%EC%95%A0%22%20%ED%95%99%EC%83%9D"

    while True:
        searchUrl = "http://search.chosun.com/search/news.search?query=" + queryString + "&pageno=" + str(pageCount) + "&orderby=news&naviarraystr=&kind=&cont1=&cont2=&cont5=&categoryname=%EC%A1%B0%EC%84%A0%EC%9D%BC%EB%B3%B4&categoryd2=&c_scope=&sdate=&edate=&premium="
        pageContainItemCount = get_aticle_list(searchUrl)
        print("searchUrl : "+searchUrl)
        print("pageCount : "+str(pageCount))
        print("pageContainItemCount : "+str(pageContainItemCount))
        pageCount += 1
        if pageContainItemCount <= 0:
            break

    print("list total count : "+str(len(urlList)))


def get_aticle_list(url):
    rq = get(url)
    soup = BeautifulSoup(rq.content.decode('utf-8', 'replace'), 'html.parser')
    contents = soup.find_all(class_='search_news')
    for item in contents:
        dtTag = item.find('dt')
        aTag = dtTag.find('a')
        print(str(aTag["href"]))
        urlList.append(str(aTag["href"]))

    return len(contents)



def get_data(url):
    request = get(url)
    print("html1 : "+str(request.content))

    rand_value = randint(1, 5)
    print("rand_value : "+str(rand_value))
    time.sleep(rand_value)


    session = Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }

    html = session.get(url, headers=headers).content
    print("html2 : "+str(html))

    soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
    #soup = BeautifulSoup(request.content, "html.parser", from_encoding="utf-8")

    date = soup.find(class_='news_date')
    dateStr = date.text.replace('입력 ', '')
    print("dateStr : "+dateStr)

    title = soup.find(attrs={'id': 'news_title_text_id'})
    contentsTag = soup.find_all(class_='par')
    link = url
    print("title : "+title.text)

    contentsString = ""
    for div in contentsTag:
        if contentsString:
            contentsString = contentsString + " " + div.text
        else:
            contentsString = div.text

    write_ws.append([dateStr, title.text, "조선일보", contentsString, url])

    return contentsString

#query = input("검색어 입력: ")

# Sheet1에다 입력
write_ws = write_wb.active

# 행 단위로 추가
write_ws.append(["date", "title", "source", "contents", "link"])
'''
print('------------------')
chosun_aticle_list(query,s_date,e_date)

for urlItem in urlList:
    get_data(urlItem)
'''
print('------------------')


get_data("http://news.chosun.com/svc/content_view/content_view.html?contid=2001031270234")

# 엑셀로 저장하기 위한 변수
RESULT_PATH = 'D:/'  # 결과 저장할 경로
now = datetime.now()  # 파일이름 현 시간으로 저장하기
# 새로 만들 파일이름 지정
outputFileName = '%s-%s-%s  %s시 %s분 %s초 merging.xlsx' % (
    now.year, now.month, now.day, now.hour, now.minute, now.second)
#write_wb.save(RESULT_PATH + outputFileName)