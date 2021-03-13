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
import datetime

# エラーの時のログ、成功時のログなどをそれぞれ設定しておいて、スクレイピングの処理をしているコードの中にtry関数で入れ込んでいく。
# if成功したら成功したログを残す、  elseエラーが出たらエラーのログを残す。
# と言った具合に事前に「こういうログを残したい」というのを定義しておいて処理の中に埋め込んでいく。

# Seleniumをあらゆる環境で起動させるChromeオプション
options = Options()
options.add_argument('--disable-gpu');
options.add_argument('--disable-extensions');
options.add_argument('--proxy-server="direct://"');
options.add_argument('--proxy-bypass-list=*');
options.add_argument('--start-maximized');
# options.add_argument('--headless'); # ※ヘッドレスモードを使用する場合、コメントアウトを外す
# study02/log/log_###DATETIME###.log
LOG_FILE_PATH = 'study02/log/log_###DATETIME###.log'
DRIVER_PATH = './chromedriver'
# カレントディレクトリのchromedriverを指定
# DRIVER_PATH = '/Users/Kenta/Desktop/Selenium/chromedriver' # ローカル
# DRIVER_PATH = '/app/.chromedriver/bin/chromedriver'        # heroku
log_file_path=LOG_FILE_PATH.replace("###DATETIME###",datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))


### ログファイルおよびコンソール出力
def log(txt):
    now=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    logStr = '[%s: %s] %s' % ('log',now , txt)
    # ログ出力
    with open(log_file_path,mode='a', encoding='utf-8_sig') as f:
        f.write(logStr + '\n')
    print(logStr)

def main ():
    log("処理開始")
    search_keyword = input('検索したいキーワードを入力してください　:')
    log("検索キーワード:{}".format(search_keyword))

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
        # # ポップアップを閉じる
        # driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass

    driver.find_element_by_class_name('topSearch__text').send_keys(search_keyword)
    driver.find_element_by_class_name("topSearch__button").click()

    titles = []
    welfares = []
    incomes = []
    count = 0

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
            try:
                selector = 'tbody tr:nth-child(5) td'
                elem_income = elem_companybox.find_element_by_css_selector(selector)
                money = elem_income.text
                incomes.append(money)
                print(money)
                log("{}件目成功".format(count))
                count+=1
            except:
                money = 'none'
                incomes.append(money)
                log("{}件目成功".format(count))
                count+=1


        driver.find_element_by_class_name("iconFont--arrowLeft").click()
        # 次のページをクリック

    log("処理完了 成功件数: {} 件".format(count))

    df = pd.DataFrame()
    df['会社名'] = titles
    df['仕事内容'] = welfares
    df['年収'] = incomes


    df.to_csv('求人情報.csv',index=False)

    driver.quit()

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
