# -*- encoding: utf-8 -*-
import requests
import lxml.html
import urllib.request
import urllib.parse
import pandas as pd
import re
from lxml.cssselect import CSSSelector
import pickle
from time import sleep
import sqlite3
import pickle

#title_txt =[]
review_txt = []
Location = []
review_rate = []
Date_of_Experience = []
body = []
all_info = []
#rpf = []#review_page_ref

# データベースに接続する
conn = sqlite3.connect('tripadvisor.db')
cur = conn.cursor()

#テーブルの作成
#cur.execute('''CREATE TABLE archtectural_building (spot_name text, geo text, sir_review text, sir_usr text, sir_date text, sir_rate integer, sir_place text)''')

sleep(3)

cur.execute('select spot_name, spot_url from spot_url_w_category_2category where spot_name = "archtectural_building" limit 5 offset 5')#あと4つ
spot_url_w_category = cur.fetchall()

review_count_list = []
category_name_list = []
for row in spot_url_w_category:
    each_url = row[1]
    r = requests.get(each_url)
    html = r.text
    # HTMLをHtmlElementオブジェクトにする
    root = lxml.html.fromstring(html)
    # XPathを指定して該当する要素のリストを得る
    number_of_review_tag = root.xpath('//div[@class="ui_header h4 counts"]')
    number_of_reivew = number_of_review_tag[0].text_content().replace(",","").strip(" results ")
    #NoR は number_of_review
    NoR = int(number_of_reivew)
    review_count_list.append(NoR)
    category_name_list.append(row[0])


for i,row in enumerate(spot_url_w_category):
    spot_url = row[1].replace("-Reviews-","-Reviews-or{}-")
    NoR = review_count_list[i]
    if NoR > 201:
        page_range = range(0,200,10)
    else:
        page_range = range(0,NoR,10)

    each_user_all = []
    for page in page_range:
        # HTMLソースを得る
        url1 = spot_url.format(page)
        r = requests.get(url1)
        html = r.text
        # HTMLをHtmlElementオブジェクトにする
        root = lxml.html.fromstring(html)
        # XPathを指定して該当する要素のリストを得る
        #review本文
        hrefs = root.xpath('//div/a[starts-with(@href, "/ShowUserReviews")]/@href')
        #print(hrefs)
        #print(len(hrefs))
        #geoの情報を得る
        geo = root.xpath('//a[@class="link"]')
        #spot nameの情報を得る
        spot_name = root.xpath('//h1[@class="ui_header h1"]')
        #user name
        usr_names = root.xpath('//*[@class="info_text"]/div[1]')
        #print(len(usr_names))
        #Date of Experienceの情報を得る
        DoEs = root.xpath('//*[@class="prw_rup prw_reviews_stay_date_hsx"]')
        #print(len(DoEs))
        #各口コミを取得
        review_divs=root.xpath('//*[@class="review-container"]')
        #print(len(review_divs))

        #print(review_div)
        No_count = 0
        j = 0
        for i in range(10):
            each_review = []
        #------------------divisionごとにserch---------------------------
            each_review.append(spot_name[0].text_content())
            each_review.append(geo[0].text_content())
            print(each_review)
            #口コミが書いてある部分を取り出して、htmlで表示
            try:
                review_div2 = lxml.html.tostring(review_divs[i],encoding='UTF-8')
            except IndexError:
                continue

            #Lacationタグを探すAttributeError
            #use_loc = re.search(r'class="userLoc"', review_div2.decode('UTF-8'))
            try:
                use_loc = re.search(r'class="userLoc"', review_div2.decode('UTF-8'))
            except AttributeError:
                use_loc = None
            #print(use_loc)

            #画像タグを探す
            pic = re.findall(r'class="photoContainer "', review_div2.decode('UTF-8'))

            #ratingを探す
            rating50 = re.search(r'ui_bubble_rating bubble_50', review_div2.decode('UTF-8'))
            rating45 = re.search(r'ui_bubble_rating bubble_45', review_div2.decode('UTF-8'))
            rating40 = re.search(r'ui_bubble_rating bubble_40', review_div2.decode('UTF-8'))
            rating35 = re.search(r'ui_bubble_rating bubble_35', review_div2.decode('UTF-8'))
            rating30 = re.search(r'ui_bubble_rating bubble_30', review_div2.decode('UTF-8'))
            rating25= re.search(r'ui_bubble_rating bubble_25', review_div2.decode('UTF-8'))
            rating20 = re.search(r'ui_bubble_rating bubble_20', review_div2.decode('UTF-8'))
            rating15= re.search(r'ui_bubble_rating bubble_15', review_div2.decode('UTF-8'))
            rating10= re.search(r'ui_bubble_rating bubble_10', review_div2.decode('UTF-8'))
            rating05= re.search(r'ui_bubble_rating bubble_05', review_div2.decode('UTF-8'))
            rating00= re.search(r'ui_bubble_rating bubble_00', review_div2.decode('UTF-8'))

            #review本文をeach_reviewへappend
            href = hrefs[i]
            url2 = 'https://www.tripadvisor.co.uk'+ href
            r2 = requests.get(url2)
            html2 = r2.text
            root2 = lxml.html.fromstring(html2)
            review = root2.xpath("//span[@class='fullText ']")
            if review == []:
                each_review.append('')
            else:
                reviews = review[0].text_content()
            #print(review2)
                each_review.append(reviews)

            #usrネームをeach_reviewへappend
            usr_name = usr_names[i].text_content()
            each_review.append(usr_name)

            #旅行日をeach_reviewへappend
            DoE = DoEs[i]
            date = DoE.text_content().replace("Date of experience: ","")
            each_review.append(date)

            #評点をeach_reviewへappend
            #ratingタグの種類によって評点がわかるようになっているので、タグに応じた評点をreview_rateに追加
            if rating50 != None:
                each_review.append(5.0)

            elif rating45 != None:
                each_review.append(4.5)

            elif rating40 != None:
                each_review.append(4.0)

            elif rating35 != None:
                each_review.append(3.5)

            elif rating30 != None:
                each_review.append(3.0)

            elif rating25 != None:
                each_review.append(2.5)

            elif rating20 != None:
                each_review.append(2.0)

            elif rating15 != None:
                each_review.append(1.5)

            elif rating10 != None:
                each_review.append(1.0)

            elif rating05 != None:
                each_review.append(0.5)

            else:
                each_review.append(0)

            #Locationをeach_reviewへappend
            #Locationのタグ有無によって、リストがずれてしまうので、それを調整しながらUser Locationを追加している
            if use_loc == None:
                #nonカウンターを作って通し番号から引いて、インデックスを作成
                No_count += 1
                home2 = "NO LOCATION"
                each_review.append(home2)

            else:
                homes = root.xpath('//div[@class="userLoc"]')
                index = i - No_count
                home1 = homes[index].text_content()
                each_review.append(home1)


            each_user_all.append(each_review)

            sir_spot = each_review[0]
            sir_geo = each_review[1]
            sir_review = each_review[2]
            sir_usr = each_review[3]
            sir_date = each_review[4]
            sir_rate = each_review[5]
            sir_place = each_review[6]

            cur.execute("insert into archtectural_building values( ?, ?, ?, ?, ?, ?, ?)", [ sir_spot, sir_geo, sir_review, sir_usr, sir_date, sir_rate, sir_place])

            conn.commit()
            #print(each_user_all)
             #print(len(each_user_all))
    print(len(each_user_all))
    all_info.append(each_user_all)
        #print(all_info)
print(len(all_info))
