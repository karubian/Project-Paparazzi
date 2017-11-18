import feedparser
import threading
import time

thread_pool = [];
sabah = "https://www.sabah.com.tr/rss/sondakika.xml"
# hurriyet = "https://www.hurriyet.com.tr/rss/magazin"
# hürriyet eski haberleri veriyor rssi düzgün değil
haberturk = "http://www.haberturk.com/rss/magazin.xml"




def get_rss(rss_url):
    rss_array = [];
    d = feedparser.parse(rss_url)
    rss_array = d['entries'].copy()
    while (1):
        d = feedparser.parse(rss_url)
        rss_item_count = len(d['entries'])
        if (rss_array[0]['link'] == d['entries'][0]['link']):
            # It means no new rss item
            print("no new")
        else:
            # print(d['feed']['title'])
            # print(len(d['entries']))
            for i in range(rss_item_count):
                if (rss_array[i]['link'] != d['entries'][i]['link']):
                    continue
                print(i + " tane yeni haber")
                for j in range(i):
                    print("write to database " + j)
                    print(d['entries'][j]['link'])
                # print(d['entries'][i]['title'])
                # print(d['entries'][i]['link'])
        print('sleep for 5 minutes')
        time.sleep(300)
        print('i woke up')


try:
    thread_pool.append(threading.Thread(target=get_rss, args=(sabah,)))
    # thread_pool.append(threading.Thread(target=get_rss, args=(hurriyet)))
    thread_pool.append(threading.Thread(target=get_rss, args=(haberturk,)))

except:
    print("za")

for elem in thread_pool:
    elem.start()

for elem in thread_pool:
    elem.join()
