from bs4 import BeautifulSoup
from requests import get
from urllib.parse import unquote


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