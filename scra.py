import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

def save_to_csv(filename, products):
    # CSVファイルを開いて商品名を書き込む
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for product in products:
            writer.writerow([product])

def amazon_get(search_keyword):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    service = Service('/opt/homebrew/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)

    driver.get('https://www.amazon.co.jp/')
    driver.implicitly_wait(5)
    sleep(2)

    search_input = driver.find_element(By.CSS_SELECTOR, 'div.nav-search-field > input')
    search_input.send_keys(search_keyword)
    driver.find_element(By.CSS_SELECTOR, 'div.nav-right > div > span > input').click()
    sleep(3)  # 検索結果が表示されるまで待つ

    # 顧客レビューのランキングで検索結果をソート
    sort_select = Select(driver.find_element(By.ID, 's-result-sort-select'))
    sort_select.select_by_value('review-rank')
    sleep(3)  # ソート結果が反映されるまで待つ

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    product_elements = soup.find_all('span', class_='a-size-base-plus a-color-base a-text-normal')
    product_names = [elem.get_text() for elem in product_elements[:10]]  # 上位10商品の名前を取得

    driver.quit()
    return product_names

if __name__ == '__main__':
    keyword = input("Enter search keyword: ")
    product_names = amazon_get(keyword)

    # CSVファイルに商品名を保存
    save_to_csv('amazon_products.csv', product_names)

    print(f"Saved the following products for '{keyword}':")
    for name in product_names:
        print(name)
