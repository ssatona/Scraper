# -*- encoding: utf-8 -*-
import requests
import lxml.html
import urllib.request
import urllib.parse
import pandas as pd
import re
import category_url_list
from lxml.cssselect import CSSSelector
import pickle
from time import sleep
import sqlite3
import pickle
from lxml.html import document_fromstring


# データベースに接続する
conn = sqlite3.connect('tripadvisor.db')
c = conn.cursor()

#テーブルの作成
c.execute('''CREATE TABLE spot_url_w_category_2category (spot_name text, spot_url text)''')


all_category_url = []

for category in category_url_list.category_list:
    # HTMLソースを得る
    r = requests.get(category)
    html = r.text
    # HTMLをHtmlElementオブジェクトにする
    root = lxml.html.fromstring(html)
    # XPathを指定して該当する要素のリストを得る
    hrefs = root.xpath('//div[@class="listing_title  title_with_snippets "]/a')
    #all_category_url.append(hrefs)
    #次のページ
    category_p2 = category.replace("Kyoto_Kyoto","oa30-Kyoto_Kyoto")
    r2 = requests.get(category_p2)
    html2 = r2.text
    # HTMLをHtmlElementオブジェクトにする
    root2 = lxml.html.fromstring(html2)
    # XPathを指定して該当する要素のリストを得る
    hrefs2 = root2.xpath('//div[@class="listing_title  title_with_snippets "]/a')
    sum_hrefs = hrefs + hrefs2
    all_category_url.append(sum_hrefs)

print(len(all_category_url))


for category_name, category_url in zip(category_url_list.category_name,all_category_url):
    for i in range(60):
        each_spot = category_url[i].get("href")
        comp_url_each_spot = "https://www.tripadvisor.co.uk{}".format(each_spot)
        c.execute("insert into spot_url_w_category_2category values( ?, ?)", [ category_name, comp_url_each_spot])
        conn.commit()
        print(category_name,comp_url_each_spot)
