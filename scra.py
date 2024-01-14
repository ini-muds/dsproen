import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

def create_db():
    conn = sqlite3.connect('amazon_products.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (name TEXT)''')
    conn.commit()
    conn.close()

def save_to_db(products):
    conn = sqlite3.connect('amazon_products.db')
    c = conn.cursor()
    for product in products:
        c.execute("INSERT INTO products VALUES (?)", (product,))
    conn.commit()
    conn.close()

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
    sleep(2)  # 検索結果が表示されるのを待つ

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    product_elements = soup.find_all('span', class_='a-size-base-plus a-color-base a-text-normal')
    product_names = [elem.get_text() for elem in product_elements[:10]]  # 上位10商品の名前を取得

    driver.quit()
    return product_names

if __name__ == '__main__':
    create_db()
    keyword = input("Enter search keyword: ")
    product_names = amazon_get(keyword)
    save_to_db(product_names)

    print(f"Saved the following products for '{keyword}':")
    for name in product_names:
        print(name)
