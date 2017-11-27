# -*- coding: utf-8 -*-
import http.client
import sys
import pymongo
import json
import datetime
import requests
from bs4 import BeautifulSoup
import time
import traceback
import logging


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
                logging.error("Tried 2 times but still no meaningful response so skip")
                error_flag = 1
                #skipped_urls.append(url)
                return article_text, error_flag
            time.sleep(5)
            logging.error("-_- Sleep -_-")
            try_count += 1
            continue
    c = result.content
    error_flag = 0
    soup = BeautifulSoup(c, "html5lib")
    try:
        article = soup.find("div", {"class": "news-detail-text"}).find_all('p')
        for element in article:
            article_text += '\n' + ''.join(element.find_all(text=True))
    except Exception as err:
        #error_urls.append(url)
        error_flag = 1
        logging.error("Exception ", exc_info=1)
        logging.error(url)
    return article_text, error_flag

uri = 'mongodb://localhost:27017/paparazzi'
client = pymongo.MongoClient(uri)
db = client.get_database('paparazzi')

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

logging.basicConfig(
        format="%(asctime)s [%(threadName)-8.8s]  %(message)s",
        handlers=[
            logging.FileHandler("{0}/{1}.log".format(".", "hurriyet")),
            logging.StreamHandler(sys.stdout)
        ])

for path in paths:
    for x in range(0,99999,50):
        logging.error("Requesting results starting at : " + x.__str__() + " from path : '" + path + "'")
        keep_trying = True
        res = None
        while (keep_trying):
            try:
                conn = http.client.HTTPSConnection("api.hurriyet.com.tr")
                conn.request("GET", "/v1/articles?$filter=Path%20eq%20'" + path + "'&$top=50&%24skip=" + x.__str__(),
                             headers=headers)
                res = conn.getresponse()
                if res.getcode() != 200:
                    raise Exception("Response code not 200")
                keep_trying = False
            except:
                logging.error("Exception ", exc_info=1)
                keep_trying = True

        data = json.loads(res.read().decode())
        if(len(data) == 0):
            logging.error("No more articles in path : '" + path + "'")
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


        news = db['raw_articles']
        news.insert_many(data)

        client.close()


