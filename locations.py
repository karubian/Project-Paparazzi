# -*- coding: utf-8 -*-
import csv
import codecs
import pandas as pd
import io

# with open("TR.csv", 'rb') as csvfile:
#     df = pd.read_csv(csvfile,encoding="utf-8",delimiter=";")
# with codecs.open('TR.csv', encoding="iso 8859-9") as the_file:
#     ad = the_file.readlines()

# for i in range(len(tuples)):
#   a, b = tuples[i]
#   print(a,b)

a = pd.read_clipboard()
print(a)

a = {
    "il": {
        "iller": [
            {"name":"Ankara","İlçeler":["John Doe","asda"],"koordinatlar":[]},
            {"name":"İstanbul","İlçeler":["John Doe","asda"],"koordinatlar":[]}
        ],
    },
    "otherstuff": {
        "thing": [[1,42],[2,2]]
     }
}
# recent move
celebrity = {
    "name":"shf",
    "popularity":234,
    "main_article":21,
    "related_article":234,
    "last_article":"link*",
    "locations": [
        {"name": "ankara", "value":3},
        {"name": "istanbul", "value": 5},
    ]
}

