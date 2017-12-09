# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import datetime
import time
import json
import pymongo
import logging
import sys

uri = 'mongodb://127.0.0.1:27017/paparazzi'
client = pymongo.MongoClient(uri)
db = client.get_database('paparazzi')

news_path = "/kelebek/magazin/"

error_urls = []
skipped_urls = []

logging.basicConfig(
        format="%(asctime)s [%(threadName)-8.8s]  %(message)s",
        handlers=[
            logging.FileHandler("{0}/{1}.log".format(".", "rssDetail")),
            logging.StreamHandler(sys.stdout)
        ])

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
                logging.error("Tried 2 times but still no meaningful response so skip")
                error_flag = 1
                skipped_urls.append(url)
                return article_text, error_flag
            time.sleep(5)
            logging.error("-_- Sleep -_-")
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
            logging.error(res)
            rssDetail = db["rssDetail"]
            rssDetail.insert_one(res)
    except:
        error_urls.append(url)
        logging.error("Exception ", exc_info=1)

    return article_text


def get_article_detail_sabah(post_url):
    url = post_url
    article_text = ''
    res = ""
    has_next_page = True
    while has_next_page:
        result = ''
        try:
            result = requests.get(url)
        except:
            skipped_urls.append(url)
            logging.error("Exception ", exc_info=1)
            logging.error("Exception occured on link : " + url)
            return

        error_flag = 0
        try:
            soup = BeautifulSoup(result.content, "html.parser")
            article_type = soup.find("meta",{"name":"tagContentType"})["content"]
            if article_type == "haber":
                article_type = "article"
                date = soup.find("meta", {"itemprop": "dateModified"})['content']
                date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
                
                article = soup.find("div", {"class": "newsBox"}).find_all('p')
                for element in article:
                    article_text = article_text + '\n' + ''.join(element.find_all(text=True))

                next_page = soup.find("li", {"class": "next"})
                if next_page is None:
                    has_next_page = False
                else:
                    next_page = soup.find("li", {"class": "next"}).find("a")["href"]

                if (has_next_page):
                    splitted_url = url.split("=")
                    if len(url.split("?")) > 1:
                        splitted_url[-1] = str(next_page).split("=")[-1]
                        url = "=".join(splitted_url)
                    else:
                        url += next_page
            
                localId = soup.find("input",{"name":"ArticleId"})["value"]
                keywords = soup.find("meta",{"name":"news_keywords"})["content"]
                if soup.find("figure", {"class": "newsImage"}) == None:
                    media = ""
                else:
                    media = soup.find("figure", {"class": "newsImage"}).img["src"]


            else:
                article_type = "gallery"
                date_text = soup.find("div",{"name","textInfo"}).find_all("span")[-1].text
                date_part = date_text.split("\r\n")
                date_text_day = date_part[1].split(":")[1].strip()
                date_text_time = date_part[2].strip()
                date = date_text_day + "T" +  date_text_time
                date = datetime.datetime.strptime(date, "%d.%m.%YT%H:%M")
                json_string = soup.find_all("script",{"type":"text/javascript"})[5].text
                localId = json_string[json_string.find("?haber")-36:json_string.find("?haber")]
                keywords = soup.find("meta",{"itemprop":"keywords"})["content"]
                text_elements = soup.find_all("figcaption")
                for item in text_elements:
                    article_text = article_text + item.text
                has_next_page = False
                media = soup.find("meta",{"itemprop":"thumbnailUrl"})["content"]
        

            title = soup.find("meta", {"itemprop": "name"})['content']

            # for item in soup.find_all("div", {"class": "photo-news-list-img"}):
            #     media_array.append(item.img["data-img-src"])

            description = soup.find("meta",{"name":"Description"})["content"]
            res = {
                "localId": localId,
                "date": date,
                "source": "sabah",
                "contentType": article_type,
                "url": post_url,
                "hash": "",
                "description": description,
                "location": "",
                "famousName": [],
                "tags": keywords.split(","),
                "media": media,
                "title": title,
                "text": article_text
            }
        except:
            logging.error("Exception ", exc_info=1)
            logging.error("Exception occured on link : " + url)
    logging.error(res)
    rssDetail = db["rssDetail"]
    rssDetail.insert_one(res)
    return article_text

