import feedparser
import time
from threading import Thread

thread_pool = [];
sabah = "https://www.sabah.com.tr/rss/gunaydin.xml"
#hurriyet = "https://www.hurriyet.com.tr/rss/magazin"
#hürriyet eski haberleri veriyor rssi düzgün değil
haberturk = "http://www.haberturk.com/rss/magazin.xml"

def get_rss(rss_url, rss_item_count):
    d = feedparser.parse(rss_url)
    print(d['feed']['title'])
    print(len(d['entries']))
    for i in range(rss_item_count):
        print(d['entries'][i]['title'])
        print(d['entries'][i]['link'])


try:
    thread_pool.append(Thread(target=get_rss, args=(sabah,30)))
    #thread_pool.append(Thread(target=get_rss, args=(hurriyet,49)))
    thread_pool.append(Thread(target=get_rss, args=(haberturk,20)))

    # _thread.start_new_thread(get_rss, (sabah, 30))
    # _thread.start_new_thread(get_rss, (hurriyet, 49,))
    # _thread.start_new_thread(get_rss, (haberturk, 20,))
except:
    print("za")

for elem in thread_pool:
    elem.start()

for elem in thread_pool:
    elem.join()


# import _thread
# import time
#
# # Define a function for the thread
# def print_time( threadName, delay):
#    count = 0
#    while count < 5:
#       time.sleep(delay)
#       count += 1
#       print ("%s: %s" % ( threadName, time.ctime(time.time()) ))
#
# # Create two threads as follows
# try:
#    _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
#    _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
# except:
#    print ("Error: unable to start thread")
#
# while 1:
#    pass
