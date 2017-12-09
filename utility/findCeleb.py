import codecs
import json

def editList():
    old_file = open("result.txt", encoding="utf8",mode="r+")
    celebrity_array = []
    with old_file as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        for celeb_name in content:
            if celeb_name.find("(") == -1:
                celebrity_array.append(celeb_name)
            else:
                celeb_name = celeb_name.split("(")[0].strip()
                celebrity_array.append(celeb_name)
    with codecs.open('clean_celebrities.txt', 'a', encoding="utf-8") as the_file:
        for celebrity in celebrity_array:
            the_file.write(celebrity+"\n")
    # you may also want to remove whitespace characters like `\n` at the end of each line


def getCelebArray():
    data = json.load(open("50_haber.json"))
    celebrity_file = open("clean_celebrities.txt", encoding="utf8",mode="r+")
    celebrity_array = []
    with celebrity_file as f:
        celebrity_array = f.readlines()
    for i in range(len(celebrity_array)):
        celebrity_array[i] = celebrity_array[i].replace("\n","")
    return celebrity_array
    # listFoundCelebs(celebrity_array,data)

def listFoundCelebs(celebrity_array,data):
    for post in data["Text"]:
        total_occurrences = 0
        article_anchors = {}
        for item in celebrity_array:
            occurrence = post.count(item)
            total_occurrences = total_occurrences + occurrence
            if occurrence > 0:
                article_anchors[item] = occurrence
                # print(str(occurrence))
                # print(item)
        print("Total occurrence of the post is " + str(total_occurrences))
        for key in article_anchors:
            print(key + " " + str(round(getNormalizedValue(total_occurrences,article_anchors[key]),2)))

def getNormalizedValue(total_occurrences,occurrence):
    return occurrence / total_occurrences

getCelebArray()

"""
name :
popularity : 234545.32
locations : [ankara : 0.234, esenler: 123]

"""