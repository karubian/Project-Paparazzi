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
    try:
        d = feedparser.parse(rss_url)
        rss_array = d['entries'].copy()
        print(threading.currentThread().name + " is working on RSS URL: " + rss_url)
        while (1):
            d = feedparser.parse(rss_url)
            rss_item_count = len(d['entries'])
            if (rss_array[0]['link'] == d['entries'][0]['link']):
                # It means no new rss item
                print("No new articles in " + threading.currentThread().name)
            else:
                for i in range(1,rss_item_count):
                    if (rss_array[i]['link'] == d['entries'][i]['link']):
                        break
                print("Found " + str(i) + " new articles in " + threading.currentThread().name)
                for j in range(i):
                    print(d['entries'][j]['link'])
            print(threading.currentThread().name + ' is sleeping for 5 minutes')
            time.sleep(300)
            print(threading.currentThread().name + ' has woken up')
    except:
        print("Something went wrong in " + threading.currentThread().name)
        print(threading.currentThread().name + ' is sleeping for 5 minutes')
        time.sleep(300)
        print(threading.currentThread().name + ' has woken up')
        get_rss(rss_url)


try:
    thread_pool.append(threading.Thread(target=get_rss, args=(sabah,)))
    #thread_pool.append(threading.Thread(target=get_rss, args=(hurriyet)))
    thread_pool.append(threading.Thread(target=get_rss, args=(haberturk,)))

except:
    print("za")

for elem in thread_pool:
    elem.start()

for elem in thread_pool:
    elem.join()
