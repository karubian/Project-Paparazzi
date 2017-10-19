import http.client
import sys
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

paths = ["/kelebek/365-gun-iyi-yasam/",
"/kelebek/arcelikin-gozunde-tum-anneler-kralicedir/",
"/kelebek/astroloji/",
"/kelebek/bir-karede-istanbul/",
"/kelebek/blog/",
"/kelebek/blog/dilara-gozalan/",
"/kelebek/keyif/dugun-mevsimi/",
"/kelebek/gurme/",
"/kelebek/hayat/",
"/kelebek/blog/hilal-meric/",
"/kelebek/hurriyet-cumartesi/",
"/kelebek/hurriyet-pazar/",
"/son-dakika-haberleri/kelebek/",
"/kelebek/keyif/",
"/kelebek/stil/kombin-sayfasi/",
"/kelebek/magazin/",
"/kelebek/blog/pinar-oznur/",
"/kelebek/gurme/restoranlar-haberleri/",
"/kelebek/saglik/",
"/kelebek/stil/",
"/kelebek/televizyon/",
"/kelebek/yarim-kalan-hayatlar/"]

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
            article['_id'] = article['Id']
            del article['Id']
            # Because the date formats differ from one article to another we have to check both formats
            try:
                article['CreatedDate'] = datetime.datetime.strptime(article['CreatedDate'], "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                article['CreatedDate'] = datetime.datetime.strptime(article['CreatedDate'], "%Y-%m-%dT%H:%M:%S%fZ")

            try:
                article['ModifiedDate'] = datetime.datetime.strptime(article['ModifiedDate'], "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                article['ModifiedDate'] = datetime.datetime.strptime(article['ModifiedDate'], "%Y-%m-%dT%H:%M:%S%fZ")

            try:
                article['StartDate'] = datetime.datetime.strptime(article['StartDate'], "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                article['StartDate'] = datetime.datetime.strptime(article['StartDate'], "%Y-%m-%dT%H:%M:%S%fZ")

        kelebek = db['kelebek_all']
        kelebek.insert_many(data)


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

