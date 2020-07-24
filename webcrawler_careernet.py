#!/usr/bin/env python
# coding: utf-8

# gget required packages
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
import time

# generate web scrapping time automatically
import datetime

# chromedriver path on my localhost
chrome_driver_path = '/Users/ting11222001/Downloads/chromedriver'
# careernet's main course url
url = 'http://www.careernet.org.tw/n/default.php?name=class_list'
# execute chromedriver in background
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options = options, executable_path = chrome_driver_path)
# implicitly_wait for 5 sec
driver.implicitly_wait(5)
driver.get(url)

# driver scrap main page of careernent
html = driver.page_source
soup = bs(html, 'lxml')

category_list = soup.select('#boundary > table > tbody > tr > td:nth-child(1)')
title_list = soup.select('#boundary > table > tbody > tr > td:nth-child(2) > a')
date_list = soup.select('#boundary > table > tbody > tr > td:nth-child(3)')

# all links of each listed course on main page
href_list = []
for i in title_list:
    href_list.append('https://www.careernet.org.tw/n/' + i.get('href'))
# print('共有 ' + str(len(href_list)) + ' 筆資料')

# final list
final_list = []

# store the length of course links
course_number = len(href_list)
# course_number = 2 for testing only

# enter each course's info page to get their category, start date, course title
for i in range(0, course_number):
    print('正在處理第' + str(i) + ' 筆資料')
    dic = {}
    dic['today'] = str(datetime.datetime.now().date())
    dic['category'] = category_list[i].text
    dic['title'] = title_list[i].text
    dic['start_date'] = date_list[i].text
    # use selenium driver
    driver.get(href_list[i])
    driver.implicitly_wait(5)
    try:
        content = driver.find_element_by_xpath("//tr[2]/td/div[1]/fieldset[1]")
        dic['content'] = content.text
    except:
        dic['content'] = 'NaN'
    try:
        price = driver.find_element_by_xpath("//fieldset/ul/li[2]/span[contains(text(),'課程收費')]")
        if price.text.find('單堂') > 0:
            dic['price'] = price.text[price.text.find('課程收費：單堂')+7:price.text.find('元')].replace(',','')
        else:
            dic['price'] = price.text[price.text.find('課程收費：')+5:price.text.find('元')].replace(',','')
    except:
        dic['price'] = 'NaN'
    try:
        audience = driver.find_element_by_xpath("//tr[2]/td/div[1]/fieldset[3]")
        dic['audience'] = audience.text
    except:
        dic['audience'] = 'NaN'
    try:
        location = driver.find_element_by_xpath("//fieldset/ul/li[4]/span[contains(text(),'地點')]")
        dic['location'] = location.text
    except:
         dic['location'] = 'NaN'
    final_list.append(dic)

# close webdriver
driver.quit()

# print(final_list)

# check data using dataframe
# raw_data = {
#     'today': str(datetime.datetime.now().date()),
#     'title': [i['title'] for i in final_list],
#     'category': [i['category'] for i in final_list],
#     'start_date': [i['start_date'] for i in final_list],
#     'content': [i['content'] for i in final_list],
#     'price': [i['price'] for i in final_list],
#     'audience': [i['audience'] for i in final_list],
#     'location': [i['location'] for i in final_list],
#     'href': href_list, #for checking only
# }
# pd.set_option('display.max_rows', None)
# df = pd.DataFrame(raw_data)

# write data into pickle format
import pickle
with open('edu_careernet_tiff.pickle', 'wb') as f:
    pickle.dump(final_list, f)

# read pickle back as "data"
with open('edu_careernet_tiff.pickle', 'rb') as f:
    data = pickle.load(f)
# print(data)

# insert data into SQL
from sqlalchemy import create_engine
def insert_sql(data):
    df = pd.DataFrame(data)
    engine = create_engine('mysql+pymysql://tiffany:admin123@192.168.56.123:3306/education')
    df.to_sql('careernet', engine, index = False)
# insert_sql(data)


