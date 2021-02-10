# -*- encoding: utf-8 -*-
import requests
import lxml.html
import urllib.request
import urllib.parse
import pandas as pd
import re
import spots_list
from lxml.cssselect import CSSSelector
import pickle
from time import sleep

#title_txt =[]
review_txt = []
Location = []
review_rate = []
Date_of_Experience = []
body = []
all_info = []
#rpf = []#review_page_ref


for spot in spots_list.area_jp:
    each_user_all = []
    for page in range(0,930,10):
        # HTMLソースを得る
        url1 = spot.format(page)
        r = requests.get(url1)
        html = r.text
        # HTMLをHtmlElementオブジェクトにする
        root = lxml.html.fromstring(html)
        # XPathを指定して該当する要素のリストを得る
        #review本文
        hrefs = root.xpath('//div/a[starts-with(@href, "/ShowUserReviews")]/@href')
        #print(hrefs)
        #print(len(hrefs))
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
            url2 = 'https://www.tripadvisor.jp'+ href
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
            print(reviews)

            #usrネームをeach_reviewへappend
            usr_name = usr_names[i].text_content()
            each_review.append(usr_name)

            #旅行日をeach_reviewへappend
            DoE = DoEs[i]
            date = DoE.text_content().replace("訪問時期：","")
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

            #画像を取得
            if pic != None:
                pictures = root2.xpath('//div/span[@class="imgWrap "]/img')
                #print(len(pictures))
                for k in range(len(pic)):
                    try:
                        picture = pictures[k].get("data-lazyurl")
                        each_review.append(picture)
                    except IndexError:
                        picture = "error"
                        each_review.append(picture)
                    #print(picture.get("data-lazyurl"))

            each_user_all.append(each_review)
            #print(each_user_all)
             #print(len(each_user_all))
    print(len(each_user_all))
    all_info.append(each_user_all)
        #print(all_info)
print(len(all_info))

#------------------------Pickleで保存------------------------------------------------------
with open('gion930_jp.pickle', 'wb') as building:
    pickle.dump(all_info,building)




#画像を取得
#pictures = root.xpath('//div/span[@class="imgWrap "]/img')
#print(len(pictures))
#print(pictures)
#for pic in pictures:
#    print(pic.get("data-lazyurl"))
