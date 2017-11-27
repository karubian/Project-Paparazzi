# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pymongo
import time
import traceback

uri = 'mongodb://BerkSefkatli:berk1996@ds159254.mlab.com:59254/paparazzi'
client = pymongo.MongoClient(uri)
db = client.get_database('paparazzi')
print(db.kelebek_all.count())

news_path = "/kelebek/magazin/"

error_urls = []
skipped_urls = []


def get_article_detail(post_info):
    url = post_info["Url"]
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
                skipped_urls.append(url)
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
        error_urls.append(url)
        error_flag = 1
        traceback.print_exc()
    return article_text,error_flag


def insert_details(path):
    news_posts = db.kelebek_all.find({"Path": path})
    i = 0
    for doc in news_posts:
        print(doc["Url"])
        if get_article_detail(doc)[1] == 0:
            db.magazine_details_berk.insert_one({'Title': doc["Title"], 'Url': doc["Url"],
                                            "ModifiedDate": doc["ModifiedDate"],
                                            "_id": doc["_id"], "Description": doc["Description"],
                                            "Tags": doc["Tags"],
                                            "Text": get_article_detail(doc)})
        print(i)
        i = i + 1

insert_details(news_path)
errorfile = open('errors.txt', 'w')
for item in error_urls:
  errorfile.write("%s\n" % item)
skippedfile = open('errorsSkipped.txt', 'w')
for item in skipped_urls:
    skippedfile.write("%s\n" % item)