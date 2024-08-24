from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

chromedriver_path = "drivers/chromedriver-win64/chromedriver.exe"

chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument("--log-level=1")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--log-level=1")

service = Service(chromedriver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.zapimoveis.com.br/aluguel/apartamentos/pr+curitiba/1-quarto/"

try:
    driver.get(url)
    time.sleep(6) 

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    apartment_divs = soup.find_all("div", {"class": "ListingCard_result-card__Pumtx"})
    
    for i in apartment_divs:
        div_1 = i.find("div", {"class": "ListingCard_header__wrapper__sI7ZX"})
        section_1 = div_1.find("section")
        div_2 = section_1.find("div")
        title_h2 = div_2.find("h2")
        print(title_h2.text)
        #title_text = title_h2.find("h2").text
        #print(title_h2)


except Exception as e:
    print(f"An error occurred: {e}")

#finally:
    #driver.quit()