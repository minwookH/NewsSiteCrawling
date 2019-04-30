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

def naver_aticle_list(query):
    pageCount = 1
    queryString = quote(query)
    print("queryString : "+queryString)
    #queryString = "%22%EB%B0%9C%EB%8B%AC%EC%9E%A5%EC%95%A0%22%20%ED%95%99%EC%83%9D"

        #https://search.naver.com/search.naver?&where=news&query=%22%EC%9E%90%ED%8F%90%22%20%2B%ED%95%99%EC%83%9D&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&start=2050&refresh_start=0

    while True:
        searchUrl = "https://search.naver.com/search.naver?&where=news&query="+queryString+"&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&start="+str(pageCount)+"&refresh_start=0"
        pageContainItemCount = get_aticle_url(searchUrl)
        print("searchUrl : "+searchUrl)
        print("pageCount : "+str(pageCount))
        print("pageContainItemCount : "+str(pageContainItemCount))
        pageCount += 10
        if pageContainItemCount <= 0 or pageCount >= 100:
            break

    print("list total count : "+str(len(urlList)))


def get_aticle_url(url):
    #rq = get("https://search.naver.com/search.naver?query=%ED%98%84%EB%8C%80%EC%97%94%EC%A7%80%EB%8B%88%EC%96%B4%EB%A7%81&where=news&ie=utf8&sm=nws_hty")
    rq = get(url)
    soup = BeautifulSoup(rq.content, "html.parser", from_encoding="utf-8")


    #_sp_each_url





    contents = soup.find_all('a', class_='_sp_each_url')
    print("contents count : "+str(len(contents)))
    for item in contents:

        print("item : " + str(item))

        if item.text == "네이버뉴스":
            print("네이버뉴스 맞음!! : ")
            print("href : "+str(item["href"]))
            urlList.append(str(item["href"]))



        '''
        dtTag = item.find('dt')
        aTag = dtTag.find('a')
        print(str(aTag["href"]))
        urlList.append(str(aTag["href"]))
        '''

    return len(contents)



def get_data(url):
    print("------------------------------")


    session = Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }

    print("url : "+str(url))
    html = session.get(url, headers=headers).content
    print("html : "+str(html))

    soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
    #soup = BeautifulSoup(request.content, "html.parser", from_encoding="utf-8")

    dateString = ""
    title = ""
    pressName = ""
    contentsString = ""
    try:
        date = soup.find('span', class_='t11')
        # dateStr = date.text.replace('입력 ', '')
        print("dateStr : " + date.text)
        dateString = date.text
        title = soup.title.string

       # print("title1 : " + str(soup.title))
        print("title2 : " + soup.title.string)

        # title = soup.find(attrs={'id': 'news_title_text_id'})
        contentsTag = soup.find_all(attrs={'id': 'articleBodyContents'})
        link = url
        # print("title : "+title.text)

        #print("contentsTag count : " + str(len(contentsTag)))
        for div in contentsTag:
            if contentsString:
                contentsString = contentsString + " " + div.text
            else:
                contentsString = div.text

        print("contentsString : " + contentsString)

        pressLogo = soup.find('div', class_='press_logo')
        pressName = pressLogo.find('img')['title']
        print("pressName : " + str(pressName))
        # attrs={'id': 'news_title_text_id'}

        write_ws.append([dateString, title, pressName, contentsString, url])
    except Exception as error:
        print("error : " + str(error))


    rand_value = randint(1, 2)
    time.sleep(rand_value)

    return contentsString

query = input('검색어 입력("자폐"+학생): ')

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

ttt = "https%3A//news.naver.com/main/read.nhn%3Fmode%3DLSD%26mid%3Dsec%26sid1%3D101%26oid%3D009%26aid%3D0004348449"

queryString = unquote(ttt)
#print('queryString : '+queryString)

#get_data(queryString)
naver_aticle_list(query)

for urlItem in urlList:
    get_data(urlItem)
#get_aticle_list("")

# 엑셀로 저장하기 위한 변수
RESULT_PATH = 'D:/'  # 결과 저장할 경로
now = datetime.now()  # 파일이름 현 시간으로 저장하기
# 새로 만들 파일이름 지정
outputFileName = '%s-%s-%s  %s시 %s분 %s초 merging.xlsx' % (
    now.year, now.month, now.day, now.hour, now.minute, now.second)
write_wb.save(RESULT_PATH + outputFileName)