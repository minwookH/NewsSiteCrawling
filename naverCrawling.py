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

def naver_aticle_list(query, count):
    pageCount = 1
    queryString = quote(query)
    print("queryString : "+queryString)
    #queryString = "%22%EB%B0%9C%EB%8B%AC%EC%9E%A5%EC%95%A0%22%20%ED%95%99%EC%83%9D"

    while True:
        searchUrl = "https://search.naver.com/search.naver?&where=news&query="+queryString+"&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&start="+str(pageCount)+"&refresh_start=0"
        pageContainItemCount = get_aticle_url(searchUrl)
        pageCount += 10
        if pageContainItemCount <= 0 or pageCount >= int(count):
            break

    print("list total count : "+str(len(urlList)))


def get_aticle_url(url):
    rq = get(url)
    soup = BeautifulSoup(rq.content, "html.parser", from_encoding="utf-8")

    contents = soup.find_all('a', class_='_sp_each_url')
    print("contents count : "+str(len(contents)))
    for item in contents:
        if item.text == "네이버뉴스":
            print("네이버뉴스 맞음!! : ")
            print("href : "+str(item["href"]))
            urlList.append(str(item["href"]))


    return len(contents)



def get_data(url):
    session = Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    }

    print("url : "+str(url))
    html = session.get(url, headers=headers).content

    soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")

    dateString = ""
    title = ""
    pressName = ""
    contentsString = ""
    try:
        date = soup.find('span', class_='t11')
        dateString = date.text
        title = soup.title.string
        title = title.replace(': 네이버 뉴스', '')

        contentsTag = soup.find_all(attrs={'id': 'articleBodyContents'})

        for div in contentsTag:
            if contentsString:
                contentsString = contentsString + " " + div.text
            else:
                contentsString = div.text

        contentsString = contentsString.replace('// flash 오류를 우회하기 위한 함수 추가', '')
        contentsString = contentsString.replace('function _flash_removeCallback() {}', '')
        print("contentsString : " + contentsString)

        pressLogo = soup.find('div', class_='press_logo')
        pressName = pressLogo.find('img')['title']
        print("title : " + title+", pressName : " + str(pressName))

        write_ws.append([dateString, title, pressName, contentsString, url])
    except Exception as error:
        print("error : " + str(error))


    #rand_value = randint(1, 2)
    #time.sleep(rand_value)

    return contentsString

query = input('검색어 입력("자폐"+학생): ')
count = input('검색될 최대 기사수(1000) 입력: ')

# Sheet1에다 입력
write_ws = write_wb.active

# 행 단위로 추가
write_ws.append(["date", "title", "source", "contents", "link"])

naver_aticle_list(query, count)

for urlItem in urlList:
    get_data(urlItem)

# 엑셀로 저장하기 위한 변수
RESULT_PATH = 'D:/'  # 결과 저장할 경로
now = datetime.now()  # 파일이름 현 시간으로 저장하기
# 새로 만들 파일이름 지정
outputFileName = '%s-%s-%s  %s시 %s분 %s초 merging.xlsx' % (
    now.year, now.month, now.day, now.hour, now.minute, now.second)
write_wb.save(RESULT_PATH + outputFileName)