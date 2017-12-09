import pymongo
import findCeleb


uri = 'mongodb://localhost:27017/paparazzi'
client = pymongo.MongoClient(uri)
db = client.get_database('paparazzi')

celebs = findCeleb.getCelebArray()
print(celebs)
for item in celebs:
    celebrity = {
        "name": item,
        "popularity": 0,
        "num_main_articles": 0,
        "related_articles": 0,
        "last_article": "",
        "locations": []
    }
    db["celebrities"].insert_one(celebrity)
    client.close()