from bs4 import BeautifulSoup
from requests import get
from urllib.parse import unquote
from urllib.parse import quote
from datetime import datetime

from openpyxl import Workbook

urlList = []
write_wb = Workbook()

def chosun_aticle_list(query,s_date,e_date):
    pageCount = 1
    queryString = quote(query)
    #queryString = "%22%EB%B0%9C%EB%8B%AC%EC%9E%A5%EC%95%A0%22%20%ED%95%99%EC%83%9D"

    while True:
        searchUrl = "http://search.chosun.com/search/news.search?query=" + queryString + "&pageno=" + str(pageCount) + "&orderby=news&naviarraystr=&kind=&cont1=&cont2=&cont5=&categoryname=%EC%A1%B0%EC%84%A0%EC%9D%BC%EB%B3%B4&categoryd2=&c_scope=&sdate=" + s_date + "&edate=" + e_date + "&premium="
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
    soup = BeautifulSoup(request.content.decode('utf-8', 'replace'), 'html.parser')

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

query = input("검색어 입력: ")
s_date = input("시작날짜 입력(2019.01.04):")  # 2019.01.04
e_date = input("끝날짜 입력(2019.01.05):")  # 2019.01.05

# Sheet1에다 입력
write_ws = write_wb.active

# 행 단위로 추가
write_ws.append(["date", "title", "source", "contents", "link"])

print('------------------')
chosun_aticle_list(query,s_date,e_date)

for urlItem in urlList:
    get_data(urlItem)

print('------------------')

# 엑셀로 저장하기 위한 변수
RESULT_PATH = 'D:/'  # 결과 저장할 경로
now = datetime.now()  # 파일이름 현 시간으로 저장하기
# 새로 만들 파일이름 지정
outputFileName = '%s-%s-%s  %s시 %s분 %s초 merging.xlsx' % (
    now.year, now.month, now.day, now.hour, now.minute, now.second)
write_wb.save(RESULT_PATH + outputFileName)