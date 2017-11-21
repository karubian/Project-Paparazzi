import feedparser
import threading
import time

thread_pool = []
sabah = "https://www.sabah.com.tr/rss/anasayfa.xml"
sabah2 = "https://www.sabah.com.tr/rss/sondakika.xml"
haberturk = "http://www.haberturk.com/rss/magazin.xml"
anadoluajans = "http://aa.com.tr/tr/rss/default?cat=guncel"
# hurriyet = "https://www.hurriyet.com.tr/rss/magazin"
# hürriyet eski haberleri veriyor rssi düzgün değil


def get_rss(rss_url):
    try:
        new_rss = feedparser.parse(rss_url)
        sorted_old_rss_array = sorted(new_rss['entries'], key=lambda article: article['published_parsed'],
                                      reverse=True)
        print(threading.currentThread().name + " is working on RSS URL: " + rss_url)
        while True:
            new_rss = feedparser.parse(rss_url)
            rss_item_count = len(new_rss['entries'])
            sorted_new_rss_array = sorted(new_rss['entries'], key=lambda article: article['published_parsed'],
                                          reverse=True)
            if sorted_old_rss_array[0]['link'] == sorted_new_rss_array[0]['link']:
                # It means no new rss item
                print("No new articles in " + threading.currentThread().name)
            else:
                for i in range(1,rss_item_count):
                    if sorted_old_rss_array[0]['link'] == sorted_new_rss_array[i]['link']:
                        break
                print("Found " + str(i) + " new articles in " + threading.currentThread().name)
                for j in range(i):
                    # write the new articles to the database here
                    print(sorted_new_rss_array[j]['link'])
                sorted_old_rss_array = sorted_new_rss_array.copy()
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
    thread_pool.append(threading.Thread(target=get_rss, args=(sabah2,)))
    thread_pool.append(threading.Thread(target=get_rss, args=(haberturk,)))
    thread_pool.append(threading.Thread(target=get_rss, args=(anadoluajans,)))

except:
    print("Creating threads failed.")

for elem in thread_pool:
    elem.start()

for elem in thread_pool:
    elem.join()
