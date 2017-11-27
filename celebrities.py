# -*- coding: utf-8 -*-
import codecs


def readCelebrities():
    with open("celebrities.txt", encoding="utf-8") as f:
        celebrityList= f.readlines()
        print(len(celebrityList))
    return celebrityList


def separateRepetitiveItem():
    seen = set()
    uniq = []
    for x in celebrityList:
        if x not in seen:
            uniq.append(x)
            seen.add(x)
    return uniq

def writeToFile():
    with codecs.open('result.txt', 'a' , encoding="utf-8") as the_file:
        for celebrity in celebrityList:
            the_file.write(celebrity)


def findWordIndText(word,text):
    if word in text:
        print("success")


celebrityList = readCelebrities()
celebrityList = separateRepetitiveItem()
print(len(celebrityList))
writeToFile()
