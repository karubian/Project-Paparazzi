# -*- coding: utf-8 -*-
import http.client
import pymongo
import json
import datetime

uri = 'mongodb://BerkSefkatli:berk1996@ds159254.mlab.com:59254/paparazzi'
client = pymongo.MongoClient(uri)
db = client.get_database('paparazzi')

conn = http.client.HTTPSConnection("api.hurriyet.com.tr")

headers = {
    'accept': "application/json",
    'apikey': "4c67720b046a4743aba6979181505cef"
    }

paths = ["/kelebek/gurme/",
"/kelebek/hayat/",
         # hayat not finished
"/kelebek/blog/hilal-meric/",
"/kelebek/hurriyet-cumartesi/",
"/kelebek/hurriyet-pazar/",
"/son-dakika-haberleri/kelebek/",
"/kelebek/keyif/",
         # keyif not finished 6250
"/kelebek/magazin/",
"/kelebek/blog/pinar-oznur/",
"/kelebek/televizyon/"]

#
for path in paths:
    for x in range(0,1000000,50):
        print("Requesting results starting at : " + x.__str__() + " from path : '" + path + "'")
        conn.request("GET", "/v1/newsphotogalleries?$filter=Path%20eq%20'" + path + "'&$top=50&%24skip=" + x.__str__(),
                     headers=headers)
        res = conn.getresponse()

        while(res.getcode() != 200):
            print(res.getcode().__str__() + " fail " + res.read().decode('utf-8'))
            conn.request("GET", "/v1/newsphotogalleries?$filter=Path%20eq%20'" + path + "'&$top=50&%24skip=" + x.__str__(),
                         headers=headers)
            res = conn.getresponse()

        data = json.loads(res.read())
        if(len(data) == 0):
            print("No more galleries in path : '" + path + "'")
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


        news = db['news']
        try:
            print(data)
            #news.insert_many(data)
        except pymongo.errors.BulkWriteError as bwe:
            # Incase of duplicate errors.
            print(bwe.details)




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

client.close()

