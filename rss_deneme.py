import feedparser

d = feedparser.parse('http://www.hurriyet.com.tr/rss/magazin')

print(d['feed']['title'])

print(len(d['entries']))

for i in range(50):
    print(d['entries'][i]['title'])
    print(d['entries'][i]['link'])



