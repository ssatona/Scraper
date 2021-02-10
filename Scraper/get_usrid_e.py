# -*- encoding: utf-8 -*-
from selenium import webdriver
import lxml.html
import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import requests
import urllib.request
import urllib.parse
import pandas as pd
import re
import Kyoto_spot
import pickle
from time import sleep


#------------------------chrome制御--------------------------------------------------
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)
url = 'https://www.tripadvisor.co.uk.html'
driver.get(url)
#--------------------------------------------------------------------------------------
spot_name_all = []
id_list_all = []
rate_list_all = []
review_url_list = []
body = []
body_non = []

name_list = ['kiyomizu']
for cnt,spot in enumerate(Kyoto_spot.url_list):
    #spot name作るのであればここで、手打ちでも、インデックスでも
#------------------------------page制御-----------------------------------------------------
    for pro in range(1):
        try:
            id_list = []
            spot_name = []
            rate_list = []
            page = 770 #This number shows the number of current page later
            while True:
            #continue until getting the last page
                print(spot.format(page))
                print("Starting to get posts...")
                url = spot.format(page)
                driver.get(url)

        #--------------------------------User ID 取得-----------------------------------------------
                m_l = driver.find_elements_by_class_name('member_info')
                div = driver.find_elements_by_xpath('//div[@class="ui_column is-9"]/span[1]')
                #print(div)
                for i,x in enumerate(m_l):
                    htmlcode = div[i].get_attribute("outerHTML")
                    rating = htmlcode[htmlcode[0].find('ui_bubble_rating bubble_')+38:39]
                    print(rating)
                    #int(rating)
                    rate = int(rating) / 10
                    print(rate)
                    rate_list.append(rate)

                    x.click()
                    sleep(8)

                    element = driver.find_element_by_xpath('//*[@id="BODY_BLOCK_JQUERY_REFLOW"]/span/div[3]/div/div/div/a')
                    element = driver.find_element_by_class_name('body_text')
                    element = element.find_element_by_tag_name('a')
                    sleep(8)
                    id = element.get_attribute("href")
                    sleep(5)
                    #id = driver.find_elements_by_class_name('href')
                    id_list.append(id)
                    spot_name.append(name_list[cnt])

                    c_f =driver.find_elements_by_class_name('ui_close_x')
                    c_f[-1].click()
                    sleep(3)

        #--------------------------------pageをめくる作業----------------------------------------------
                #driver.find_elements_by_xpath('//a[@class="nav next taLnk ui_button primary"]')
                if driver.find_elements_by_xpath('//a[@class="nav next taLnk ui_button primary"]') != []:
                    page+=10
                    driver.implicitly_wait(10)
                    print("Moving to next page......")
                    sleep(10)

        except Exception as e: # 必要であれば失敗時の処理
            print("retry")
            id_list_all.append(id_list)
            spot_name_all.append(spot_name)
            rate_list_all.append(rate_list)
            print("no pager exist anymore")


            sleep(2)

            #-------------------pickle化------------------
            if pro == 0:
                print(id_list_all)
                print(len(id_list_all))
                print(spot_name_all)
                print(len(spot_name_all))
                print(rate_list_all)
                print(len(rate_list_all))
                with open('id_list1_non_comp00000.pickle', 'wb') as id_list_p_non_comp0:
                    pickle.dump(id_list_all,id_list_p_non_comp0)

                for i in range(len(id_list_all)):
                    list_of_isr = [spot_name_all[i],id_list_all[i],rate_list_all[i]]
                    body_non.append(list_of_isr)

                with open('spot_id_rate_kiyomizu5.pickle', 'wb') as spot_id_rate_kiyomizu:
                    pickle.dump(body_non,spot_id_rate_kiyomizu)
            #elif pro == 1:
            #    with open('id_list1_non_comp1.pickle', 'wb') as id_list_p_non_comp1:
            #        pickle.dump(id_list_all,id_list_p_non_comp1)
            #elif pro == 2:
            #    with open('id_list1_non_comp2.pickle', 'wb') as id_list_p_non_comp2:
            #        pickle.dump(id_list_all,id_list_p_non_comp2)
            pass
        else:
            break  # 失敗しなかった時はループを抜ける

"""
    id_list_all.append(id_list)
    spot_name_all.append(spot_name)
    rate_list_all.append(rate_list)
    print("no pager exist anymore")
    #print(id_list_all)
    print(len(id_list_all))
    #print(spot_name_all)
    print(len(spot_name_all))
    #print(rate_list_all)
    print(len(rate_list_all))

    sleep(2)

#-------------------pickle化------------------
with open('id_list1.pickle', 'wb') as id_list_p:
    pickle.dump(id_list_all,id_list_p)

#----------------table---------------
for i in range(len(id_list_all)):
    list_of_isr = [id_list_all[i],spot_name_all[i],rate_list_all[i]]
    body.append(list_of_isr)

print(body)
"""

sleep(2)
#.click()
driver.close()
driver.quit()
