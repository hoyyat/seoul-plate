from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
import time

client = MongoClient('mongodb+srv://test:sparta@cluster0.akqwn.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

driver = webdriver.Chrome('C:\\Users\le123\Desktop\chromedriver_win32\chromedriver.exe')
driver.implicitly_wait(5)
driver.get('https://www.siksinhot.com/taste?upHpAreaId=9&hpAreaId=&isBestOrd=Y')

for i in range(40):
    try:
        더보기 = driver.find_element_by_class_name('btn_sMore')
        더보기.click()
        time.sleep(0.1)
    except:
        break

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

plates = soup.select('#tabMove1 > div > ul > li > div > a')
plate_num = 0

for i in range(1150):
    img = plates[i].select_one('span > img')['src']
    title = plates[i].select_one('div > div.box_tit > strong').text
    place = plates[i].select_one('div > ul:nth-child(3) > li').text
    content = plates[i].select_one('div > p').text

    doc = {
        'plate_num': plate_num,
        'img': img,
        'title': title,
        'place': place,
        'content': content
    }
    db.plates.insert_one(doc)
    plate_num += 1
