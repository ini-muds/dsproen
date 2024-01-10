from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_amazon_top_products(search_query):
    try:
        print("Setting up WebDriver...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        print("Accessing Amazon website...")
        driver.get("https://www.amazon.co.jp")

        print("Searching for the product...")
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)

        print("Waiting for search results to load...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-component-type='s-search-result']"))
        )
        time.sleep(2)

        print("Collecting search results...")
        products = driver.find_elements(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")
        top_products = [product.text for product in products[:10]]

        print("Closing the browser...")
        driver.quit()

        return top_products

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()
        return []


search_query = ""


print("Getting top products for the search query...")
top_products = get_amazon_top_products(search_query)
print("Top products:", top_products)