import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

def create_or_append_to_csv():
    # CSVファイルを開く（存在しない場合は作成）
    with open('amazon_products.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        return writer

def save_to_csv(products, writer):
    # 商品名をCSVファイルに保存
    for product in products:
        writer.writerow([product])

def amazon_get(search_keyword):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    service = Service('/opt/homebrew/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)

    driver.get('https://www.amazon.co.jp/')
    driver.implicitly_wait(5)
    sleep(1)

    driver.find_element(By.CSS_SELECTOR, 'div.nav-search-field > input').send_keys(search_keyword)
    driver.find_element(By.CSS_SELECTOR, 'div.nav-right > div > span > input').click()
    sleep(2)  # 検索結果が表示されるまで待つ

    # 顧客レビューのランキングで検索結果をソート
    sort_select = Select(driver.find_element(By.ID, 's-result-sort-select'))
    sort_select.select_by_value('review-rank')
    sleep(2)  # ソート結果が反映されるまで待つ

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    product_elements = soup.find_all('span', class_='a-size-base-plus a-color-base a-text-normal')
    product_names = [elem.get_text() for elem in product_elements[:10]]  # 上位10商品の名前を取得

    driver.quit()
    return product_names

if __name__ == '__main__':
    keyword = input("Enter search keyword: ")
    product_names = amazon_get(keyword)

    # CSVファイルへの書き込み用ライターを取得
    csv_writer = create_or_append_to_csv()
    save_to_csv(product_names, csv_writer)

    print(f"Saved the following products for '{keyword}':")
    for name in product_names:
        print(name)
