# -*- coding: utf-8 -*-
import csv
import pandas as pd
import io

with open("TR.csv", 'rb') as csvfile:
    df = pd.read_csv(csvfile,encoding="WINDOWS-1254",delimiter=";")

tr = [tuple(x) for x in df.values]

# for i in range(len(tuples)):
#   a, b = tuples[i]
#   print(a,b)

print(tr)
