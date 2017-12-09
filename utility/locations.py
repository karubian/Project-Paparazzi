# -*- coding: utf-8 -*-
import pandas as pd
import pymongo

uri = 'mongodb://127.0.0.1:27017/paparazzi'
client = pymongo.MongoClient(uri)
db = client.get_database('paparazzi')

# Copy the contents of dirty_location.txt prior to running the code.
city_data = pd.read_csv("../data/il_koordinat.txt",delimiter=" ", header=None)
district_data = pd.read_csv("../data/ilce_koordinat.txt",delimiter=" ", header=None)
#data = pd.read_clipboard(header=None)
#print(data)
iller = []
i = 0
for row in city_data.as_matrix():
    city_code = row[4].split('(')[1].split('\'')[1]
    city_name = row[5].split('\'')[1]
    latitude_first = row[6].split('\'')[1]
    longtitude_second = row[7].split('\'')[1]

    il = {
        "code": city_code,
        "name": city_name,
        "latitude": latitude_first,
        "longtitude": longtitude_second,
        "type": "city",
        "districts": []
    }
    # filtered = district_data[5].filter(like = '\''+city_code+'\'')
    # print(filtered)

    while(i < len(district_data.as_matrix())):
        if(district_data.as_matrix()[i][5] == '\''+city_code+'\','):
            district_code = district_data.as_matrix()[i][4].split('(')[1].split('\'')[1]
            district_name = district_data.as_matrix()[i][6].split('\'')[1]
            latitude_district = district_data.as_matrix()[i][7].split('\'')[1]
            longtitude_district = district_data.as_matrix()[i][8].split('\'')[1]

            il['districts'].append({
                "code": district_code,
                "name": district_name,
                "latitude": latitude_district,
                "longtitude": longtitude_district,
                "type": "district",
            })
            i = i + 1
        else:
            break

    iller.append(il)

print(iller)
locations = db["locations"]
locations.insert_many(iller)

# # recent move
# celebrity = {
#     "name":"shf",
#     "popularity":234,
#     "main_article":21,
#     "related_article":234,
#     "last_article":"link*",
#     "locations": [
#         {"name": "ankara", "value":3},
#         {"name": "istanbul", "value": 5},
#     ]
# }

