import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


# Chromeを起動する関数
def set_driver(driver_path, headless_flg):
    if "chrome" in driver_path:
        options = ChromeOptions()
    else:
        options = Options()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    if "chrome" in driver_path:
        # Chromeドライバーがバージョンアップの際に自動で更新
        return webdriver.Chrome(ChromeDriverManager().install())
    else:
        return Firefox(executable_path=os.getcwd()  + "/" + driver_path,options=options)



# main処理
def main():
    
    # 検索したいキーワードを入力する処理
    search_keyword = input('調べたいキーワードを入力してください>>>')
    
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(3)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(3)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')

    # 検索窓に入力
    driver.find_element_by_class_name("topSearch__text").send_keys(search_keyword)
    
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()
    
    time.sleep(4)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    
    # 空のDataFrame作成
    df = pd.DataFrame()
    
    # 空の会社名を入れるリスト
    company_name = []
    
    # 空の求人タイトルを入れるリスト
    job_ttl = []
    
    # 空の会社名を入れるリスト
    income_month = []
    
    # for文で一つの求人に対して・会社名・求人タイトル・給与を取得してくる
    while True:
        
        # 会社名を取得
        name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
        
        # 求人タイトルを取得
        ttl_list = driver.find_elements_by_class_name('cassetteRecruit__copy')
        
        # 給与を取得
        income_list = driver.find_elements_by_xpath("//*[contains(text(), '給与')]/following-sibling::td")
        
        for i in range(len(name_list)):
            
            # 会社名
            try:
                name = name_list[i].text
                company_name.append(name)
                # ログの書き出し
                with open('log.txt', 'a') as f:
                    f.write(f'{len(company_name)}件目\n')
                    f.write(f'{name}\n')
            except Exception as e:
                name = e
                with open('log.txt', 'a') as f:
                    f.write(f'エラー内容：{e}\n')
                pass
            
            # 求人タイトル
            try:
                ttl = ttl_list[i].text
                job_ttl.append(ttl)
                # ログの書き出し
                with open('log.txt', 'a') as f:
                    f.write(f'{ttl}\n')
            except Exception as e:
                ttl = e
                with open('log.txt', 'a') as f:
                    f.write(f'エラー内容：{e}\n')
                pass
            
            # 給与
            try:
                income = income_list[i].text
                income_month.append(income)
                # ログの書き出し
                with open('log.txt', 'a') as f:
                    f.write(f'{income}\n')
                    f.write(f'\n')
                    f.write(f'\n')
            except Exception as e:
                income = e
                with open('log.txt', 'a') as f:
                    f.write(f'エラー内容：{e}\n')
                pass
            
            # csvに取得した情報を書き出す
            df = df.append(
                {
                    '会社名': name,
                    '求人名': ttl,
                    '給与': income
                },
                ignore_index=True
            )
            
        df.index = df.index + 1
        df.to_csv("scraping_data.csv")
        
        try:
            # 次のページへボタンクリック
            driver.execute_script('document.querySelector(".iconFont--arrowLeft").click()')
            time.sleep(3)
        except Exception as e:
            print(e)
            # driver.close()
            break

    cur_url = driver.current_url
    kw_url = cur_url.split('/', 4)[4]
    add_search = input('他に調べたいキーワードを入力してください>>>>>')

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()