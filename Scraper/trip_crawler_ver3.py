import requests
import lxml.html
import urllib.request
import urllib.parse
import pandas as pd
import re


#title_txt =[]
review_txt = []
Location = []
review_rate = []
Date_of_Experience = []
body = []
#rpf = []#review_page_ref

#request = urllib.request.Request(url=url, headers=headers)
#response = urllib.request.urlopen(request)
#html = response.read().decode('utf-8')

for page in range(10,180,10):
        # HTMLソースを得る
    url1 = 'https://www.tripadvisor.co.uk/Attraction_Review-g303159-d555336-Reviews-or{}-Ise_Shrine_Ise_Jingu-Ise_Mie_Prefecture_Tokai_Chubu.html'.format(page)
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"}
    r = requests.get(url1, headers=headers)
    html = r.text
    # HTMLをHtmlElementオブジェクトにする
    root = lxml.html.fromstring(html)
    # XPathを指定して該当する要素のリストを得る
    #titles = root.xpath("//span[@class='noQuotes']")
    hrefs  = root.xpath('//div/a[starts-with(@href, "/ShowUserReviews")]/@href')
    #print(hrefs)
    #Date of Experienceの情報を得る
    DoEs = root.xpath('//*[@class="prw_rup prw_reviews_stay_date_hsx"]')
    review_div=root.xpath('//*[@class="prw_rup prw_reviews_review_resp"]')

    #print(review_div)
    No_count = 0
    for i in range(10):
        #口コミが書いてある部分を取り出して、htmlで表示
        review_div2 = lxml.html.tostring(review_div[i],encoding='UTF-8')
        #hrefタグ
        #href_tag = re.search(r'/ShowUserReviews', review_div2.decode('UTF-8'))
        #Lacationタグを探す
        use_loc = re.search(r'class="userLoc"', review_div2.decode('UTF-8'))
        #print(use_loc)
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

        #if href_tag != None:
        #    href_list  = root.xpath('//a[starts-with(@href, "/ShowUserReviews")]/@href')
        #    print(len(href_list))
        #    href = href_list[i]
        #    url2 = 'https://www.tripadvisor.co.uk/'+ href
        #    r2 = requests.get(url2)
        #    html2 = r2.text
        #    root2 = lxml.html.fromstring(html2)
        #    review = root2.xpath("//span[@class='fullText ']")
        #    reviews = review[0]
        #    review2 = reviews.text_content()
        #    review_txt.append(review2)
        #else:
        #    print("Error!!")

        #ratingタグの種類によって評点がわかるようになっているので、タグに応じた評点をreview_rateに追加
        if rating50 != None:
            review_rate.append(5.0)

        elif rating45 != None:
            review_rate.append(4.5)

        elif rating40 != None:
            review_rate.append(4.0)

        elif rating35 != None:
            review_rate.append(3.5)

        elif rating30 != None:
            review_rate.append(3.0)

        elif rating25 != None:
            review_rate.append(2.5)

        elif rating20 != None:
            review_rate.append(2.0)

        elif rating15 != None:
            review_rate.append(1.5)

        elif rating10 != None:
            review_rate.append(1.0)

        elif rating05 != None:
            review_rate.append(0.5)

        else:
            review_rate.append(0)


        #Locationのタグ有無によって、リストがずれてしまうので、それを調整しながらUser Locationを追加している
        if use_loc == None:
            #nonカウンターを作って通し番号から引いて、インデックスを作成
            No_count += 1
            home2 = "NO LOCATION"
            Location.append(home2)

        else:
            homes = root.xpath('//div[@class="userLoc"]')
            index = i - No_count
            home1 = homes[index].text_content()
            Location.append(home1)

    #reviewのtitle
    #for title in titles:
    #    t = title.text_content().replace('\n','')
    #    title_txt.append(t)

    #review本文
    for href in hrefs:
        #href1 = lxml.html.tostring(href,encoding='UTF-8').decode('UTF-8')
        url2 = 'https://www.tripadvisor.co.uk'+ href
        #print(url2)
        #rpf.append(url2)
        r2 = requests.get(url2)
        html2 = r2.text
        root2 = lxml.html.fromstring(html2)
        print(root2)

        review = root2.xpath("//span[@class='fullText ']")
        if review == []:
            print("Error")
            review_txt.append("Error")

        else:
            #print(review)
            reviews = review[0]
            review2 = reviews.text_content()
            #print(review2)
            review_txt.append(review2)

    for DoE in DoEs:
        Doe1 = DoE.text_content().strip("Date of experience:")
        Date_of_Experience.append(Doe1)

#print(hrefs)
#print(len(hrefs))
#print(Location)
#print(review_rate)
#print(len(review_rate))
print(len(Location))
#print(title_txt)
#print(review_txt)
print(len(review_txt))
#print(Date_of_Experience)
print(len(Date_of_Experience))



for i in range(len(review_txt)):
    review_list = [Location[i],review_txt[i],review_rate[i],Date_of_Experience[i]]
    body.append(review_list)
    #print(len(body))


df = pd.DataFrame(body,columns=['location','review','review_rate','Date_of_Experience'])
df.to_csv("0331_review_all_test00.csv", encoding="UTF-8")
