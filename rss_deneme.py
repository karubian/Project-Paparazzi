# -*- coding: utf-8 -*-
import feedparser
import threading
import time
import traceback
import RssDetail
import json
import logging
import sys

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
        logging.error(threading.currentThread().name + " is working on RSS URL: " + rss_url)
        while True:
            new_rss = feedparser.parse(rss_url)
            rss_item_count = len(new_rss['entries'])
            sorted_new_rss_array = sorted(new_rss['entries'], key=lambda article: article['published_parsed'],
                                          reverse=True)
            logging.error("Len old : " + str(len(sorted_new_rss_array)))
            logging.error("Len new : " + str(len(sorted_old_rss_array)))
            if sorted_old_rss_array[0]['link'] == sorted_new_rss_array[0]['link']:
                # It means no new rss item
                logging.error("No new articles in " + threading.currentThread().name)
            else:
                for i in range(1,rss_item_count):
                    if sorted_old_rss_array[0]['link'] == sorted_new_rss_array[i]['link']:
                        break
                logging.error("Found " + str(i) + " new articles in " + threading.currentThread().name)
                for j in range(i):
                    # write the new articles to the database here
                    if(rss_url.startswith("http://www.haberturk.com")):
                        logging.error(sorted_new_rss_array[j]['link'])
                        RssDetail.get_article_detail_haberturk(sorted_new_rss_array[j]['link'])
                    elif(rss_url.startswith("https://www.sabah.com.tr")):
                        logging.error(sorted_new_rss_array[j]['link'])
                        #RssDetail.get_article_detail_haberturk(sorted_new_rss_array[j]['link'])
                    elif (rss_url.startswith("http://aa.com.tr")):
                        logging.error(sorted_new_rss_array[j]['link'])
                        #RssDetail.get_article_detail_haberturk(sorted_new_rss_array[j]['link'])
                    logging.error(sorted_new_rss_array[j]['link'])
                sorted_old_rss_array = sorted_new_rss_array
            logging.error(threading.currentThread().name + ' is sleeping for 5 minutes')
            time.sleep(300)
            logging.error(threading.currentThread().name + ' has woken up')
    except:
        logging.error("Something went wrong in " + threading.currentThread().name)
        logging.error("Exception ", exc_info=1)
        logging.error(threading.currentThread().name + ' is sleeping for 5 minutes')
        time.sleep(300)
        logging.error(threading.currentThread().name + ' has woken up')
        get_rss(rss_url)


try:
    # logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    # rootLogger = logging.getLogger()
    #
    # fileHandler = logging.FileHandler("{0}/{1}.log".format(".", "logtest"))
    # fileHandler.setFormatter(logFormatter)
    # rootLogger.addHandler(fileHandler)
    #
    #
    # consoleHandler = logging.StreamHandler(sys.stdout)
    # consoleHandler.setFormatter(logFormatter)
    # rootLogger.addHandler(consoleHandler)

    logging.basicConfig(
        format="%(asctime)s [%(threadName)-8.8s]  %(message)s",
        handlers=[
            logging.FileHandler("{0}/{1}.log".format(".", "rss")),
            logging.StreamHandler(sys.stdout)
        ])
    logging.error("denemee")
    thread_pool.append(threading.Thread(target=get_rss, args=(sabah,)))
    thread_pool.append(threading.Thread(target=get_rss, args=(sabah2,)))
    thread_pool.append(threading.Thread(target=get_rss, args=(haberturk,)))
    thread_pool.append(threading.Thread(target=get_rss, args=(anadoluajans,)))

except:
    print("Creating threads failed.")
    logging.getLogger().error("Exception ", exc_info=1)

for elem in thread_pool:
    elem.start()

for elem in thread_pool:
    elem.join()
