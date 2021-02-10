from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import kyoto_best10_en
from selenium import webdriver
import lxml.html
import chromedriver_binary
#kyoto_best10_en.url_list
'''
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome('/Users/iuchiyasuhiro/Desktop/chromedriver', chrome_options=options)
'''

#URL = 'https://www.tripadvisor.co.uk/Profile/Chief_Scone_Baker'
#URL = 'https://www.tripadvisor.co.uk/Attraction_Review-g14124527-d321401-Reviews-or{}-Kiyomizu_dera_Temple-Higashiyama_Kyoto_Kyoto_Prefecture_Kinki.html'
#driver = webdriver.Chrome("/Users/iuchiyasuhiro/Desktop/chromedriver")
#driver.get(URL)

#m_l = driver.find_element_by_xpath('//li[@class="member_info"]')
#print(m_l)
#ui_button primary large
#driver.find_element_by_class_name('social-show-more-ShowMore__button_contents--1djai').click()
import time
import csv
from tqdm import tqdm

#driver.find_element_by_class_name('member_info').click()

#username reviewsEnhancements
#ele = driver.find_element_by_tag_name("h3")
#ele = driver.find_element_by_class_name('username reviewsEnhancements')
print("========== scraping中だよ(-ω-)zzz =============")
for (f,p) in enumerate(kyoto_best10_en.url_list):

    id_list=[]
    for j in tqdm(range(0,1000,10)):
        #URL = 'https://www.tripadvisor.co.uk/Attraction_Review-g14124527-d321401-Reviews-or{}-Kiyomizu_dera_Temple-Higashiyama_Kyoto_Kyoto_Prefecture_Kinki.html'.format(j)

        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=options)
        #driver = webdriver.Chrome('/Users/iuchiyasuhiro/Desktop/chromedriver', chrome_options=options)
        #driver = webdriver.Chrome("/Users/iuchiyasuhiro/Desktop/chromedriver")
        driver.get(p.format(j))
        m_l = driver.find_elements_by_class_name('member_info')

        for (i,x) in enumerate(m_l):
            x.click()

            time.sleep(0.5)
            #driver.set_script_timeout(3)
            element = driver.find_element_by_xpath('//*[@id="BODY_BLOCK_JQUERY_REFLOW"]/span/div[3]/div/div/div/a')
            element = driver.find_element_by_class_name('body_text')
            element = element.find_element_by_tag_name('a')
            id = element.get_attribute("href")

            #id = driver.find_elements_by_class_name('href')
            id_list.append(id)

            c_f =driver.find_elements_by_class_name('ui_close_x')
            c_f[-1].click()

            time.sleep(0.5)
            '''
    with open('./output/out_{}.csv'.format(f),'w') as f:
        #writer = csv.writer(f, lineterminator='\n')
        #writer = csv.writer(f)
        for i in range(len(id_list)):
            f.write(id_list[i])
            f.write(",")
            f.write('\n')
            '''



#//*[@id="BODY_BLOCK_JQUERY_REFLOW"]/span/div[3]/div/div/div/a
'''
m_l = driver.find_elements_by_class_name('member_info')
print(len(m_l))
for (i,x) in enumerate(m_l):
    time.sleep(2)
    #print(i)
    x.click()
    time.sleep(2)

    c_f = driver.find_elements_by_class_name('ui_close_x')
    c_f[-1].click()
    time.sleep(1)
'''

import time
time.sleep(5)
#<!--trkN:1-->
#.click()
driver.close()
driver.quit()
