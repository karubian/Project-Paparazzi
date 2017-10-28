import requests
from bs4 import BeautifulSoup
import pymongo
import time

# uri = 'mongodb://BerkSefkatli:berk1996@ds159254.mlab.com:59254/paparazzi'
# client = pymongo.MongoClient(uri)
# db = client.get_database('paparazzi')
# print(db.kelebek_all.count())


error_urls = []
skipped_urls = []


def get_links():
    base_url = "http://www.sabah.com.tr"
    page_count = 4300
    url = "http://www.sabah.com.tr/arama?query=&categorytype=haber&selectedcategory=magazin&page=" + str(page_count)
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c, "html5lib")

    search_caption = soup.find("div", {"class": "searchPageCaption"}).find('li')
    search_flag = str(search_caption).split(".")[0].split(" ")[-1]
    while search_flag == "bulunmuştur":
        page_figures = soup.find("div", {"id": "resultList"}).find_all('figcaption')
        for item in page_figures:
            page_links = item.find('a')
            anchor_link = page_links.get("href")
            post_title = page_links.contents[0]
            post_link = base_url + anchor_link
            print(post_link)
        page_count = page_count + 1
        print(page_count)
        url = "http://www.sabah.com.tr/arama?query=&categorytype=haber&selectedcategory=magazin&page=" + str(page_count)
        result = requests.get(url)
        c = result.content
        soup = BeautifulSoup(c, "html5lib")
        search_caption = soup.find("div", {"class": "searchPageCaption"}).find('li')
        search_flag = str(search_caption).split(".")[0].split(" ")[-1]



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


# errorfile = open('errors.txt', 'w')
# for item in error_urls:
#   errorfile.write("%s\n" % item)
# skippedfile = open('errorsSkipped.txt', 'w')
# for item in skipped_urls:
#     skippedfile.write("%s\n" % item)

get_links()