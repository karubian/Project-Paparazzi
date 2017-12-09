# -*- coding: utf-8 -*-
import http.client
import pymongo
import json
import datetime
import logging
import sys

uri = 'mongodb://localhost:27017/paparazzi'
client = pymongo.MongoClient(uri)
db = client.get_database('paparazzi')

headers = {
    'accept': "application/json",
    'apikey': "4c67720b046a4743aba6979181505cef"
    }

paths = ["/kelebek/gurme/",
"/kelebek/hayat/",
"/kelebek/magazin/",
"/kelebek/blog/pinar-oznur/",
"/kelebek/televizyon/"]



logging.basicConfig(
        format="%(asctime)s [%(threadName)-8.8s]  %(message)s",
        handlers=[
            logging.FileHandler("{0}/{1}.log".format(".", "hurriyetGallery")),
            logging.StreamHandler(sys.stdout)
        ])

for path in paths:
    for x in range(0,1000000,50):
        logging.error("Requesting results starting at : " + x.__str__() + " from path : '" + path + "'")
        keep_trying = True
        res = None
        while (keep_trying):
            try:
                conn = http.client.HTTPSConnection("api.hurriyet.com.tr")
                conn.request("GET", "/v1/newsphotogalleries?$filter=Path%20eq%20'" + path + "'&$top=50&%24skip=" + x.__str__(),
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
            logging.error("No more galleries in path : '" + path + "'")
            break

        for gallery in data:
            gallery['localId'] = gallery['Id']
            try:
                gallery['date'] = datetime.datetime.strptime(gallery['CreatedDate'], "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                gallery['date'] = datetime.datetime.strptime(gallery['CreatedDate'], "%Y-%m-%dT%H:%M:%S%fZ")

            gallery['source'] = "hürriyet"
            gallery['contentType'] = "Gallery"
            gallery['url'] = gallery['Url']
            gallery['hash'] = ""
            text = ""
            for photo in gallery['Files']:
                text += " " + photo['Metadata']['Description']

            gallery['text'] = text
            gallery['description'] = gallery['Description']
            gallery['location'] = ''
            gallery['famousName'] = []
            gallery['tags'] = gallery['Tags']
            gallery['media'] = []
            for photo in gallery['Files']:
                gallery['media'].append(photo['FileUrl'])

            gallery['title'] = gallery['Title']


            del gallery['Id']
            del gallery['ContentType']
            del gallery['Files']
            del gallery['Url']
            del gallery['ModifiedDate']
            del gallery['Path']
            del gallery['StartDate']
            del gallery['Tags']
            del gallery['Title']
            del gallery['CreatedDate']
            del gallery['Description']

            # Because the date formats differ from one article to another we have to check both formats


        news = db['raw_articles']
        try:
            news.insert_many(data)
        except pymongo.errors.BulkWriteError as bwe:
            # Incase of duplicate errors.
            logging.error(bwe.details)
logging.error("Extracting all galleries in Hurriyet API ended successfully.")
client.close()

