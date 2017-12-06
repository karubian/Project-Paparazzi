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
    findCeleb(celebrity_array,data)

def findCeleb(celebrity_array,data):
    for post in data["Text"]:
        for item in celebrity_array:
            occurence = post.count(item)
            if occurence > 0:
                print(str(occurence))
                print(item)


getCelebArray()