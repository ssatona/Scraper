from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

'''
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome('/Users/iuchiyasuhiro/Desktop/chromedriver', chrome_options=options)
'''

#URL = 'https://www.tripadvisor.co.uk/Profile/Chief_Scone_Baker'
#URL = 'https://www.tripadvisor.co.uk/Attraction_Review-g14124527-d321401-Reviews-or{}-Kiyomizu_dera_Temple-Higashiyama_Kyoto_Kyoto_Prefecture_Kinki.html'
driver = webdriver.Chrome("/Users/iuchiyasuhiro/Desktop/chromedriver")
driver.get(URL)

#m_l = driver.find_element_by_xpath('//li[@class="member_info"]')
#print(m_l)
#ui_button primary large
driver.find_element_by_class_name('social-show-more-ShowMore__button_contents--1djai').click()
#m1 = driver.find_elements_by_class_name('member_info')
#print(len(m1))
'''
m2 = driver.find_element_by_class_name('member_info').click()
m3 = driver.find_element_by_class_name('member_info').click()
'''
import time
time.sleep(5)
#<!--trkN:1-->
#.click()
driver.close()
driver.quit()
