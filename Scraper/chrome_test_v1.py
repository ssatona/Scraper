from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# ブラウザーを起動
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)

# Google検索画面にアクセス
driver.get('https://www.google.co.jp/')

# htmlを取得・表示
html = driver.page_source
print(html)

# ブラウザーを終了
driver.quit()
