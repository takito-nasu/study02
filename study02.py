from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
import logging.config
import datetime

 
# ログ設定ファイルからログ設定を読み込み
logging.config.fileConfig('logging.conf')
 
logger = logging.getLogger()
 
logger.log(20, 'info')
logger.log(30, 'warning')
logger.log(100, 'test')
 
logger.info('info')
logger.warning('warning')

# Seleniumをあらゆる環境で起動させるChromeオプション
options = Options()
options.add_argument('--disable-gpu');
options.add_argument('--disable-extensions');
options.add_argument('--proxy-server="direct://"');
options.add_argument('--proxy-bypass-list=*');
options.add_argument('--start-maximized');
# options.add_argument('--headless'); # ※ヘッドレスモードを使用する場合、コメントアウトを外す

DRIVER_PATH = './chromedriver'
# カレントディレクトリのchromedriverを指定
# DRIVER_PATH = '/Users/Kenta/Desktop/Selenium/chromedriver' # ローカル
# DRIVER_PATH = '/app/.chromedriver/bin/chromedriver'        # heroku

search_keyword = input('検索したいキーワードを入力してください　:')

# ブラウザの起動
driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)

# Webページにアクセスする
url = 'https://tenshoku.mynavi.jp/'
driver.get(url)
time.sleep(3)
 
try:
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(3)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
except:
    pass

driver.find_element_by_class_name('topSearch__text').send_keys(search_keyword)
driver.find_element_by_class_name("topSearch__button").click()

titles = []
welfares = []
incomes = []

for i in range(3):
    elems_companybox = driver.find_elements_by_class_name('cassetteRecruit__content')
    # 全体の取得

    # 会社名の取得
    for elem_companybox in elems_companybox:
        elem_name = elem_companybox.find_element_by_class_name('cassetteRecruit__name')
        title = elem_name.text.split('|')[0]
        titles.append(title)
        
    # 各項目の取得
    for elem_companybox in elems_companybox:
        elem_th = elem_companybox.find_element_by_class_name('tableCondition__body')
        item = elem_th.text
        welfares.append(item)
    
    for elem_companybox in elems_companybox:
        selector = 'tbody tr:nth-child(5) td'
        elem_income = driver.find_element_by_css_selector(selector)
        money = elem_income.text
        incomes.append(money)
        print(money)
    
    driver.find_element_by_class_name("iconFont--arrowLeft").click()
    # 次のページをクリック

df = pd.DataFrame()
df['会社名'] = titles
df['仕事内容'] = welfares
df['年収'] = incomes


df.to_csv('求人情報.csv',index=False)

driver.quit()