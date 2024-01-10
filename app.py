from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import sqlite3


def get_amazon_top_products(search_query):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get("https://www.amazon.co.jp")
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
    )
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@data-component-type='s-search-result']"))
    )
    time.sleep(2)

    products = driver.find_elements(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")
    top_products = [product.text for product in products[:10]]

    driver.quit()
    return top_products

# データベース接続の設定
conn = sqlite3.connect('amazon_products.db')
cursor = conn.cursor()

# テーブルの作成
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        product_name TEXT
    )
''')
conn.commit()

# データベースにデータを挿入し、取得する関数
def insert_and_retrieve_products(product_names):
    for name in product_names:
        cursor.execute('INSERT INTO products (product_name) VALUES (?)', (name,))
    conn.commit()

    cursor.execute('SELECT * FROM products')
    all_products = cursor.fetchall()

    for product in all_products:
        print(product)

# スクリプトの実行
search_query = "ノートパソコン"
product_names = get_amazon_top_products(search_query)
insert_and_retrieve_products(product_names)

# データベース接続のクローズ
conn.close()
