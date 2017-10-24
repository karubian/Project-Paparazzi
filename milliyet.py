from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import time

driver = webdriver.Chrome("C:\\Users\\Asus\\Downloads\\chromedriver_win32\\chromedriver.exe")
driver.get("http://www.milliyet.com.tr/magazin/")
searchButton = driver.find_element_by_class_name('srch')
searchButton.click()
searchBox = driver.find_element_by_id('inpSearchKeywordtop')
searchBox.send_keys("Şeyma Subaşı")
searchBox.send_keys(Keys.RETURN)
assert "Nothing found" not in driver.page_source
error_urls = []

list_link = []
list_page = driver.find_elements_by_xpath("//div[contains(@class,'pager')]/ul/li/a[@href]")
for page in list_page:
    list_html = driver.find_elements_by_xpath("//div[contains(@class,'row')]/ul/li/a[@href]")
    for item in list_html:
        link = item.get_attribute("href")
        list_link.append(link)
        print(link)

    try:
        elem = driver.find_element_by_link_text("ileri")
        elem.click()
    except:
        break

articleFile = open('article.txt', 'w')

def get_article_detail(post_info):
    url = post_info
    result = ''
    while result == '':
        try:
            result = requests.get(url)
        except:
            time.sleep(5)
            print("-_- Sleep -_-")
            continue

    c = result.content
    error_flag = 0
    soup = BeautifulSoup(c, "html.parser")
    article_text = ''
    try:
        article = soup.find("div", {"class": "article"}).find_all('p')
        for element in article:
            article_text += '\n' + ''.join(element.find_all(text=True))
            articleFile.write("%s\n" % article_text)
    except:
        error_urls.append(url)
        error_flag = 1
        print("bom")
    return article_text, error_flag


for link in list_link:
    get_article_detail(post_info=link)


errorFile = open('errors.txt', 'w')
for item in error_urls:
  errorFile.write("%s\n" % item)





