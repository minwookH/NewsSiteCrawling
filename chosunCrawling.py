from bs4 import BeautifulSoup
from requests import get
from urllib.parse import unquote

urlList = []

def chosunAticleList(url):

    testUrl = "http://search.chosun.com/search/news.search?query=%22%EB%B0%9C%EB%8B%AC%EC%9E%A5%EC%95%A0%22+%ED%95%99%EC%83%9D&pageno=0&orderby=news&naviarraystr=&kind=&cont1=&cont2=&cont5=&categoryname=%EC%A1%B0%EC%84%A0%EC%9D%BC%EB%B3%B4&categoryd2=&c_scope=navi&sdate=&edate=&premium="

    rq = get(testUrl)
    soup = BeautifulSoup(rq.content.decode('utf-8', 'replace'), 'html.parser')
    contents = soup.find_all(class_='search_news')
    for item in contents:
        dtTag = item.find('dt')
        aTag = dtTag.find('a')
        print(str(aTag["href"]))
        urlList.append(str(aTag["href"]))

def getData(url):
    request = get(url)
    soup = BeautifulSoup(request.content.decode('utf-8', 'replace'), 'html.parser')

    date = soup.find(class_='news_date')
    dateStr = date.text.replace('입력 ', '')
    print("dateStr : "+dateStr)

    title = soup.find(attrs={'id': 'news_title_text_id'})
    contents = soup.find_all(class_='par')
    link = url
    print("title : "+title.text)

    result = ""
    for div in contents:
        if result:
            result = result + " " + div.text
        else:
            result = div.text

    return result


url1 = "http://news.chosun.com/site/data/html_dir/2018/05/30/2018053001715.html"
url2 = "http://news.chosun.com/site/data/html_dir/2018/03/28/2018032800188.html"

print('------------------')
print(getData(url1))

print('------------------')
print(getData(url2))
print('------------------')
chosunAticleList("")