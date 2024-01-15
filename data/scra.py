import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

def save_to_csv(filename, products):
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

    # 検索入力が表示されるのを待つ
    wait = WebDriverWait(driver, 60)
    search_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="field-keywords"]')))

    search_input.send_keys(search_keyword)
    search_input.submit()

    # 検索結果が読み込まれるのを待つ
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-component-type="s-search-result"]')))

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    product_elements = soup.find_all('span', class_='a-size-base-plus a-color-base a-text-normal')
    product_names = [elem.get_text() for elem in product_elements[:40]]  # 上位20商品の名前を取得

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
