# -*- encoding: utf-8 -*-
from selenium import webdriver
import lxml.html
import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
import urllib.request
import urllib.parse
import pandas as pd
import re
import pickle
from time import sleep


usr_location = []#DB1につける情報
user_review_list = []
user_profile_list = []
reviewed_place_list = []

#------------------driver set up-----------------
options = webdriver.ChromeOptions()
#options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
#options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)

#-------------------------id_list open------------
#with open('id_list1.pickle','rb') as id_list_p:
#    id_list_all = pickle.load(id_list_p)

with open('id_list1_non_comp0.pickle','rb') as id_list_p_non_comp0:
    id_list_all = pickle.load(id_list_p_non_comp0)


#-------------------------get url-----------------
for spot in id_list_all:
    for profile in spot[:3]:
        review_url_list = []
        user_profile = []
        reviewed_place = []
        URL = '{}?tab=reviews'.format(profile)
        driver.get(URL)
        sleep(5)

#----------User Location-------------------------------------------------------------
        loc = driver.find_elements_by_xpath('//span[@class="social-member-common-MemberHometown__member_info--yYJTE social-member-common-MemberHometown__hometown--3kM9S default"]')
#DB1につける情報
        if loc == []:
            usr_location.append("None")
        else:
            usr_location.append(loc[0].text)
        print(usr_location)

        #------------get number of reviews---------------------------------
        click_p = driver.find_elements_by_xpath('//a[@class="social-member-MemberStats__link--HqVwd"]')
        click_p[0].click()
        sleep(5)

        #photoがなかったりすると該当クラスが1つしかなく、順番が狂うので-1
        click_rev_num = driver.find_elements_by_xpath('//a[@class="social-member-MemberContributionsList__link--tRQU5"]')
        print(click_rev_num)
        sleep(3)

        if len(click_rev_num) == 1 or len(click_rev_num) == 2:
            sleep(1)
            number_of_review = click_rev_num[-1].text
            sleep(1)
            print(number_of_review)

        elif len(click_rev_num) >= 3:
            sleep(1)
            number_of_review = click_rev_num[1].text
            sleep(1)
            print(number_of_review)

        else:
            click_rev_num = driver.find_elements_by_xpath('//a[@class="social-member-MemberContributionsList__link--tRQU5"]')
            sleep(3)
            print(click_rev_num)
            if len(click_rev_num) < 3:
                sleep(1)
                number_of_review = click_rev_num[-1].text
                sleep(1)
                print(number_of_review)

            elif len(click_rev_num) >= 3:
                sleep(1)
                number_of_review = click_rev_num[1].text
                sleep(1)
                print(number_of_review)

            else:
                print("error",profile)
                continue

        number_of_review_int = int(number_of_review.strip(" reviews").replace(",", ""))
        print(number_of_review_int)
        sleep(3)

        close = driver.find_elements_by_xpath('//div[@class="overlays-pieces-CloseX__close--7erra"]')
        close[0].click()
        sleep(5)

        #------------Show more クリック----------------------------------------
        try:
            driver.find_element_by_class_name("social-show-more-ShowMore__button_contents--1djai").click()

        except Exception as e:
            review = driver.find_elements_by_xpath('//div/a[starts-with(@href, "/ShowUserReviews")]')
            place = driver.find_elements_by_xpath('//div[@class="social-poi-POIObject__poi_location--3hevu social-poi-POIObject__with_bubble--bbi8o"]')
            sleep(5)
            for i in range(len(review)):
                rev = review[i]
                pla = place[i].text
                c = rev.get_attribute('href')
                review_url_list.append(c)
                user_profile.append(profile)
                reviewed_place.append(pla)
        sleep(5)

        #-------------------------ユーザーの全レビューを取得----------------------
        while True:
            rev = driver.find_elements_by_xpath('//div/a[starts-with(@href, "/ShowUserReviews")]')
            if len(rev) < number_of_review_int:
                driver.execute_script('scroll(0,document.body.scrollHeight)')
                sleep(7)
            else:
                break

        review = driver.find_elements_by_xpath('//div/a[starts-with(@href, "/ShowUserReviews")]')
        place = driver.find_elements_by_xpath('//div[@class="social-poi-POIObject__poi_location--3hevu social-poi-POIObject__with_bubble--bbi8o"]')

        for i in range(len(review)):
            rev = review[i]
            pla = place[i].text
            c = rev.get_attribute('href')
            review_url_list.append(c)
            user_profile.append(profile)
            reviewed_place.append(pla)


        #print(len(review_url_list))
        #print(review_url_list)
        #print(len(user_profile))
        #print(user_profile)
        #print(len(reviewed_place))
        #print(reviewed_place)

        user_review_list.append(review_url_list)
        user_profile_list.append(user_profile)
        reviewed_place_list.append(reviewed_place)

print(len(user_review_list))
print(user_review_list)
print(len(user_profile_list))
print(user_profile_list)
print(len(reviewed_place_list))
print(reviewed_place_list)

#-------------------pickle化------------------
with open('user_review_list.pickle', 'wb') as ur_list:
    pickle.dump(user_review_list,ur_list)

with open('user_profile_list.pickle', 'wb') as up_list:
    pickle.dump(user_profile_list,up_list)

with open('reviewed_place_list.pickle', 'wb') as rp_list:
    pickle.dump(reviewed_place_list,rp_list)


sleep(5)
#<!--trkN:1-->
#.click()
driver.close()
driver.quit()
