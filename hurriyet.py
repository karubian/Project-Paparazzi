import http.client
import sys
import pymongo
import json

uri = 'mongodb://BerkSefkatli:berk1996@ds159254.mlab.com:59254/paparazzi'
client = pymongo.MongoClient(uri)
db = client.get_database('paparazzi')

conn = http.client.HTTPSConnection("api.hurriyet.com.tr")

headers = {
    'accept': "application/json",
    'apikey': "4c67720b046a4743aba6979181505cef"
    }

x = 50
for x in range(1950,2500,50):
    print(x.__str__())
    conn.request("GET", "/v1/articles?$filter=Path%20eq%20'/kelebek/'&$top=50&%24skip=" + x.__str__(), headers=headers)
    res = conn.getresponse()
    while(res.getcode() != 200):
        print(res.getcode().__str__() + " fail " + res.read().decode('utf-8'))
        conn.request("GET", "/v1/articles?$filter=Path%20eq%20'/kelebek/'&$top=50&%24skip=" + x.__str__(), headers=headers)
        res = conn.getresponse()
    data = json.loads(res.read())
    kelebek = db['kelebek']
    kelebek.insert_many(data)
    print("bitti")

client.close()

