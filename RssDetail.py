import requests
from bs4 import BeautifulSoup
import datetime
import time
import json

# uri = 'mongodb://BerkSefkatli:berk1996@ds159254.mlab.com:59254/paparazzi'
# client = pymongo.MongoClient(uri)
# db = client.get_database('paparazzi')
# print(db.kelebek_all.count())

news_path = "/kelebek/magazin/"

error_urls = []
skipped_urls = []
################# HABERTURK ####################################################################

def get_article_detail_haberturk(post_url):
    url = post_url
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
        article_type = soup.find("meta", {"property": "og:site_name"})
        if str(article_type['content']).endswith("galeri"):
            pass
        else:
            article_info = soup.find_all('script', {'type': 'application/ld+json'})
            article_json = json.loads(article_info[0].text)
            keywords = str(json.loads(article_info[1].text)["keywords"]).split(",")
            i = 0
            for item in keywords:
                if len(item) <= 1:
                    del keywords[i]
                else:
                    keywords[i] = item.strip()
                i += 1
            news_id = soup.find("div", {"class": "reply-to-comment-area"})
            news_id = news_id.find("input", {"name": "haber_id"})["value"]

            title = article_json["headline"]
            date = article_json["datePublished"][:19:]
            datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
            media = soup.find("div",{"class":"news-detail-featured-img"})
            # for item in soup.find_all("div", {"class": "photo-news-list-img"}):
            #     media_array.append(item.img["data-img-src"])
            content_type = "article"
            description = article_json["description"]
            body = article_json["articleBody"]
            res = {
                "localId": news_id,
                "date": date,
                "source": "habertürk",
                "contentType": content_type,
                "url": post_url,
                "hash": "",
                "description": description,
                "location": "",
                "famousName": [],
                "tags": keywords,
                "media": media.img["src"],
                "title": title,
                "text": body
            }
            print(res)
            # article['source'] = "hürriyet"
            # article['contentType'] = "article"
            # article['url'] = article['Url']
            # article['hash'] = ""
            # article['description'] = article['Description']
            # article['location'] = ''
            # article['famousName'] = []
            # article['tags'] = article['Tags']
            # article['media'] = []
            # for photo in article['Files']:
            #     article['media'].append(photo['FileUrl'])
            # article['title'] = article['Title']
            # text
    except:
        error_urls.append(url)
        error_flag = 1
        print("bom")
    return article_text, error_flag


get_article_detail_haberturk("http://www.haberturk.com/nato-genel-sekreteri-cumhurbaskani-erdogan-dan-ozur-diledi-1719618")
# def insert_details(path):
#     news_posts = db.kelebek_all.find({"Path": path})
#     i = 0
#     for doc in news_posts:
#         print(doc["Url"])
#         if get_article_detail(doc)[1] == 0:
#             db.magazine_details_berk.insert_one({'Title': doc["Title"], 'Url': doc["Url"],
#                                             "ModifiedDate": doc["ModifiedDate"],
#                                             "_id": doc["_id"], "Description": doc["Description"],
#                                             "Tags": doc["Tags"],
#                                             "Text": get_article_detail(doc)})
#         print(i)
#         i = i + 1
#
# insert_details(news_path)
# errorfile = open('errors.txt', 'w')
# for item in error_urls:
#   errorfile.write("%s\n" % item)
# skippedfile = open('errorsSkipped.txt', 'w')
# for item in skipped_urls:
#     skippedfile.write("%s\n" % item)
