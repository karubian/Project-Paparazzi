import http.client
import sys
import pymongo
import json
import datetime
import requests
from bs4 import BeautifulSoup
import time


def get_article_detail(post_info):
    url = post_info["url"]
    result = ''
    article_text = ''
    try_count = 0
    while result == '':
        try:
            result = requests.get(url)
        except:
            if try_count > 2:
                print("Tried 2 times but still no meaningful response so skip")
                error_flag = 1
                #skipped_urls.append(url)
                return article_text, error_flag
            time.sleep(5)
            print("-_- Sleep -_-")
            try_count += 1
            continue
    c = result.content
    error_flag = 0
    soup = BeautifulSoup(c, "html5lib")
    try:
        article = soup.find("div", {"class": "news-detail-text"}).find_all('p')
        for element in article:
            article_text += '\n' + ''.join(element.find_all(text=True))
    except:
        #error_urls.append(url)
        error_flag = 1
        print("bom")
    return article_text, error_flag

uri = 'mongodb://BerkSefkatli:berk1996@ds159254.mlab.com:59254/paparazzi'
client = pymongo.MongoClient(uri)
db = client.get_database('paparazzi')

conn = http.client.HTTPSConnection("api.hurriyet.com.tr")

headers = {
    'accept': "application/json",
    'apikey': "4c67720b046a4743aba6979181505cef"
    }

paths = [#"/kelebek/365-gun-iyi-yasam/",
# "/kelebek/arcelikin-gozunde-tum-anneler-kralicedir/",
# "/kelebek/astroloji/",
# "/kelebek/bir-karede-istanbul/",
# "/kelebek/blog/",
# "/kelebek/blog/dilara-gozalan/",
# "/kelebek/keyif/dugun-mevsimi/",
# "/kelebek/gurme/",
# "/kelebek/hayat/",
#          # hayat not finished
# "/kelebek/blog/hilal-meric/",
# "/kelebek/hurriyet-cumartesi/",
# "/kelebek/hurriyet-pazar/",
# "/son-dakika-haberleri/kelebek/",
# "/kelebek/keyif/",
#          # keyif not finished 6250
# "/kelebek/stil/kombin-sayfasi/",
"/kelebek/magazin/",
"/kelebek/blog/pinar-oznur/",
"/kelebek/gurme/restoranlar-haberleri/",
"/kelebek/saglik/",
"/kelebek/stil/",
"/kelebek/televizyon/",
"/kelebek/yarim-kalan-hayatlar/"]

#
for path in paths:
    for x in range(0,99999,50):
        print("Requesting results starting at : " + x.__str__() + " from path : '" + path + "'")
        conn.request("GET", "/v1/articles?$filter=Path%20eq%20'" + path + "'&$top=50&%24skip=" + x.__str__(),
                     headers=headers)
        res = conn.getresponse()

        while(res.getcode() != 200):
            print(res.getcode().__str__() + " fail " + res.read().decode('utf-8'))
            conn.request("GET", "/v1/articles?$filter=Path%20eq%20'" + path + "'&$top=50&%24skip=" + x.__str__(),
                         headers=headers)
            res = conn.getresponse()

        data = json.loads(res.read())
        if(len(data) == 0):
            print("No more articles in path : '" + path + "'")
            break

        for article in data:
            article['localId'] = article['Id']
            try:
                article['date'] = datetime.datetime.strptime(article['CreatedDate'], "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                article['date'] = datetime.datetime.strptime(article['CreatedDate'], "%Y-%m-%dT%H:%M:%S%fZ")

            article['source'] = "hürriyet"
            article['contentType'] = "article"
            article['url'] = article['Url']
            article['hash'] = ""
            article['description'] = article['Description']
            article['location'] = ''
            article['famousName'] = []
            article['tags'] = article['Tags']
            article['media'] = []
            for photo in article['Files']:
                article['media'].append(photo['FileUrl'])
            article['title'] = article['Title']

            del article['Id']
            del article['ContentType']
            del article['Files']
            del article['Url']
            del article['ModifiedDate']
            del article['Path']
            del article['StartDate']
            del article['Tags']
            del article['Title']
            del article['CreatedDate']
            del article['Description']

            article['text'] = get_article_detail(article)[0]


        news = db['news']
        try:
            print(data)
            #news.insert_many(data)
        except pymongo.errors.BulkWriteError as bwe:
            # Incase of duplicate errors.
            print(bwe.details)

        client.close()




# For getting all the paths as text.
# for x in range(0,2100,50):
#     print("Requesting page : " + x.__str__())
#     conn.request("GET", "/v1/paths?$top=50&%24skip=" + x.__str__(), headers=headers)
#     res = conn.getresponse()
#     while(res.getcode() != 200):
#         print(res.getcode().__str__() + " fail " + res.read().decode('utf-8'))
#         conn.request("GET", "/v1/paths?$top=50&%24skip=" + x.__str__(), headers=headers)
#         res = conn.getresponse()
#     data = json.loads(res.read())
#     print(data)



