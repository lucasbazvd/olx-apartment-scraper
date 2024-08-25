import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

chromedriver_path = "drivers/chromedriver-win64/chromedriver.exe"

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument("--log-level=1")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.zapimoveis.com.br/aluguel/apartamentos/pr+curitiba/1-quarto/"

try:
    driver.get(url)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "ListingCard_result-card__Pumtx")))
    time.sleep(random.uniform(5, 8))  # Initial wait

    apartments_collected = set()  # To track collected apartments
    scroll_pause_time = 2
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down by a small amount
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(scroll_pause_time)

        # Check for new apartments loaded after scrolling
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        apartment_divs = soup.find_all("div", {"class": "ListingCard_result-card__Pumtx"})
        
        for i in apartment_divs:
            title = i.find("h2").text.strip()
            if title not in apartments_collected:
                apartments_collected.add(title)
                print(title)  # Print new apartments found

        # Calculate new scroll height and compare with last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Break the loop if no new content is loaded

        last_height = new_height  # Update the last height
    
    print(f"Total apartments collected: {len(apartments_collected)}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
