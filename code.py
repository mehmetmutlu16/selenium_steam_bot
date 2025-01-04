from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service)

url = "https://steamcommunity.com/market/"
browser.get(url)

time.sleep(2)

price_threshold = 300.00

try:
    while True:
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        listings = soup.find_all("div", class_="market_listing_row")

        for listing in listings:
            sticker_info = listing.find("div", class_="keychain_info")
            if sticker_info:
                item_name_block = listing.find("span", class_="market_listing_item_name")
                if item_name_block:
                    item_name = item_name_block.text.strip()
                    item_link = item_name_block.find("a", class_="market_listing_item_name_link")["href"]
                    
                    price_block = listing.find("span", class_="market_listing_price market_listing_price_with_fee")
                    if price_block:
                        price_text = price_block.text.strip().replace("$", "").replace("USD", "").strip()
                        
                        try:
                            price = float(price_text)
                        except ValueError:
                            continue
                        
                        if price < price_threshold:
                            print(f"Item Name: {item_name}")
                            print(f"Item Link: {item_link}")
                            print(f"Price: ${price}")
                            print("-" * 50)
                            
                                
        try:
            next_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.ID, "tabRecentSellListings"))
            )
            next_button.click()
        except Exception as e:
            print(f"Error clicking next button: {e}")
            break
        
        time.sleep(4) 

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    browser.quit()
