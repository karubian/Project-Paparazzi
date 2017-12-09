# -*- coding: utf-8 -*-
import csv
import codecs
import pandas as pd
import io

# Copy the contents of dirty_location.txt prior to running the code.
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

