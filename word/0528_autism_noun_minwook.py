import csv
import re
import collections
import nltk
import ckonlpy

from ckonlpy.tag import Twitter
from ckonlpy.tag import Postprocessor

articles = []

f = open('D:/pythonProject/newsSiteCrawling/190510_autismall_firstphase.csv', 'r', encoding='ms949')
data = csv.reader(f)


twitter = Twitter()
twitter.add_dictionary(['직무', '전문성', '공립학교', '교육개발원'], 'Noun')
passtags = {'Noun'}
stopwords = {'기자', '무단전재', '재배포금지'}
postprocessor = Postprocessor(twitter, passtags = passtags, stopwords = stopwords)
testList = []
#postprocessor.pos('우리아이오아이는 정말 이뻐요')
def get_data(data):
    result = postprocessor.pos(data)
    print(result)
    print("result size : "+str(len(result)))

    for item in result:
        if len(item[0]) >= 2 and len(item[0]) < 49:
            testList.append(item[0])

    print(testList)
    print("testList size : " + str(len(testList)))

    testList.clear()
    print('------------------------------')


for article in data:
    #print(article)
    get_data(article[4])
    word = [x for x in article if x]
    #print(word)
    articles.append(list(set(word)))

f.close()



nouns = []

infile = open('D:/pythonProject/newsSiteCrawling/190510_autismall_firstphase.csv', 'r', encoding='ms949')
line = infile.read()

#print('--------------------')
#print(line)
filtered = re.sub('기자', '', line)
filtered = re.sub('무단전재', '', filtered)
filtered = re.sub('재배포금지', '', filtered)

#사용자 사전 추가

twitter = Twitter()
twitter.add_dictionary('공립학교', 'Noun')
twitter.add_dictionary(['직무', '전문성'], 'Noun')
twitter.add_dictionary('교육개발원', 'Name', force=True)

noun = twitter.nouns(filtered)
print("noun : "+str(noun))
nouns.append(list(set(noun)))

wwords = []
tag_count = []

from collections import Counter
count = Counter(noun)

#조건(2글자 이상 49글자 미만)에 맞는 단어만 추출해서 wwords에 저장

for n, c in count.most_common():
    dics = {'tag': n, 'count': c}
    if len(dics['tag']) >= 2 and len(wwords) <= 49:
        tag_count.append(dics)
        wwords.append(dics['tag'])

    '''
    #추출결과 출력
    for tag in tag_count:
        print(" {:<14}".format(tag['tag']), end='\t')
        print("{}".format(tag['count']))
    '''

#한글 불용어 처리

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = "무단전재 재배포금지 저작권자"
stop_words=stop_words.split(' ')

result = []

for w in wwords:
    if w not in stop_words:
        result.append(w)

print(result)

infile.close()

import pandas as pd

dataframe = pd.DataFrame(result)
dataframe.to_csv("D:/pythonProject/resultCVS/자폐학생noun.csv", encoding='ms949')

