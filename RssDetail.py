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
            article_info_text = article_info[0].text
            article_info_tokenized = article_info_text.split("\"")
            i = 0
            for item in article_info_tokenized:
                article_info_tokenized[i] = " ".join(item.split())
                i += 1
            article_json = json.loads("\"".join(article_info_tokenized))
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
            date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
            media = soup.find("div", {"class": "news-detail-featured-img"})
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
                "media": "" if media is None else media.img["src"],
                "title": title,
                "text": body
            }
            print(res["text"])
    except:
        error_urls.append(url)
        error_flag = 1
        print("bom")
    return article_text, error_flag


def get_article_detail_sabah(post_url):
    url = post_url
    article_text = ''
    while True:
        result = ''
        try:
            result = requests.get(url)
        except:
            skipped_urls.append(url)
            return

        error_flag = 0
        soup = BeautifulSoup(result.content, "html.parser")
        try:
            article = soup.find("div", {"class": "newsBox"}).find_all('p')
            for element in article:
                article_text = article_text + '\n' + ''.join(element.find_all(text=True))

            try:
                next_page = soup.find("li", {"class": "next"}).find("a")["href"]
            except:
                break

            splitted_url = url.split("=")
            if len(url.split("?")) > 1:
                splitted_url[-1] = str(next_page).split("=")[-1]
            else:
                url += next_page

            url = "=".join(splitted_url)
            print(url)

            print(article_text)
        except:
            error_flag = 1
            print("bom")
        title = soup.find("meta", {"itemprop": "name"})['content'].text
        date = soup.find("meta", {"itemprop": "dateModified"})['content'].text
        date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        media = soup.find("div", {"class": "news-detail-featured-img"})
        # for item in soup.find_all("div", {"class": "photo-news-list-img"}):
        #     media_array.append(item.img["data-img-src"])

        #TODODOODODODODODODODO
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
            "media": "" if media is None else media.img["src"],
            "title": title,
            "text": body
        }
    return article_text, error_flag


get_article_detail_sabah("https://www.sabah.com.tr/magazin/2017/11/21/tuvana-turkay-ile-fenerbahceli-futbolcu-alper-potukun-ayrildigi-iddia-edildi?paging=1")
