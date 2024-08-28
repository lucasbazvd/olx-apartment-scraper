print("Script is starting...")
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import re
from datetime import datetime

import time
import random
import re
from datetime import datetime

chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument("--log-level=1")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--remote-debugging-port=9222")

print("Initializing WebDriver...")
driver = webdriver.Chrome(options=chrome_options)

pages = 69

def scroll_slowly(driver):
    total_height = driver.execute_script("return document.body.scrollHeight")
    scrolled = 0
    while scrolled < total_height:
        scroll_amount = random.randint(500, 1000)
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        scrolled += scroll_amount
        time.sleep(random.uniform(0.3, 0.7))
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height > total_height:
            total_height = new_height
        print(f"Scrolled: {scrolled}/{total_height} pixels")

def clean_integer(text):
    if text == "N/A":
        return None
    return int(re.sub(r'\D', '', text))

def extract_city_neighborhood(location):
    if location == "N/A":
        return "N/A", "N/A"
    parts = location.split(',')
    city = parts[0].strip()
    neighborhood = parts[1].strip() if len(parts) > 1 else "N/A"
    return city, neighborhood

def process_apartment_data(apartments):
    processed_data = []
    for apt in apartments:
        processed_apt = {
            'title': apt['title'],
            'price': clean_integer(apt['price']),
            'rooms': clean_integer(apt['rooms']),
            'area': clean_integer(apt['meters']),
            'parking': clean_integer(apt['parking']),
            'bathrooms': clean_integer(apt['bathrooms']),
            'tax': clean_integer(apt['iptu']),
            'condominium_fee': clean_integer(apt['condominio']),
            'link': apt['link']
        }
        processed_apt['city'], processed_apt['neighborhood'] = extract_city_neighborhood(apt['location'])
        processed_data.append(processed_apt)
    return processed_data


def get_apartment_data(driver):
    apartments = []
    elements = driver.find_elements(By.CSS_SELECTOR, "section.olx-ad-card.olx-ad-card--horizontal")
    for element in elements:
        # Check if the favorite button exists
        favorite_button = element.find_elements(By.CSS_SELECTOR, "button.olx-ad-card__badges-favorite-button")
        if not favorite_button:
            continue

        try:
            link = element.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
            title = element.find_element(By.CSS_SELECTOR, "h2.olx-ad-card__title").text
            price = element.find_element(By.CSS_SELECTOR, "h3.olx-ad-card__price").text
            
            # Initialize variables
            rooms = meters = parking = bathrooms = iptu = condominio = "N/A"
            
            # Extract tax and condominium_fee
            priceinfo_elements = element.find_elements(By.CSS_SELECTOR, "p.olx-ad-card__priceinfo-text")
            for info in priceinfo_elements:
                if "IPTU" in info.text:
                    iptu = info.text
                elif "Condomínio" in info.text:
                    condominio = info.text
            
            # Extract rooms, meters, parking, and bathrooms
            labels = element.find_elements(By.CSS_SELECTOR, "li.olx-ad-card__labels-item span")
            for label in labels:
                aria_label = label.get_attribute('aria-label').lower()
                if "quarto" in aria_label:
                    rooms = aria_label
                elif "metro" in aria_label:
                    meters = aria_label
                elif "vaga" in aria_label or "garagem" in aria_label:
                    parking = aria_label
                elif "banheiro" in aria_label:
                    bathrooms = aria_label
            
            # Extract location
            location_element = element.find_element(By.CSS_SELECTOR, "div.olx-ad-card__location-date-container p")
            location = location_element.text if location_element else "N/A"

            apartments.append({
                'link': link,
                'title': title,
                'price': price,
                'rooms': rooms,
                'meters': meters,
                'parking': parking,
                'bathrooms': bathrooms,
                'iptu': iptu,
                'condominio': condominio,
                'location': location
            })
        except Exception as e:
            print(f"Error extracting data from an apartment: {str(e)}")

    return apartments

all_apartments = []
for i in range(1, pages):
    url = f"https://www.olx.com.br/imoveis/aluguel/apartamentos/estado-pr/regiao-de-curitiba-e-paranagua?o={i}"
    driver.get(url)
    
    print(f"\nProcessing page {i}")
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "section.olx-ad-card.olx-ad-card--horizontal"))
    )
    
    scroll_slowly(driver)

    apartments = get_apartment_data(driver)
    all_apartments.extend(apartments)

    
    print(f"\nPage {i}: Found {len(apartments)} apartments")
    for index, apt in enumerate(apartments, 1):
        print(f"\nApartment {index}:")
        print(f"Title: {apt['title']}")
        print(f"Price: {apt['price']}")
        print(f"Rooms: {apt['rooms']}")
        print(f"Area: {apt['meters']}")
        print(f"Parking: {apt['parking']}")
        print(f"Bathrooms: {apt['bathrooms']}")
        print(f"IPTU: {apt['iptu']}")
        print(f"Condomínio: {apt['condominio']}")
        print(f"Location: {apt['location']}")
        print(f"Link: {apt['link']}")

    pause_time = random.uniform(1.0, 2.0)
    print(f"\nPausing for {pause_time:.2f} seconds before next page")
    time.sleep(pause_time)

driver.quit()

processed_data = process_apartment_data(all_apartments)
df = pd.DataFrame(processed_data)

# Save to CSV
current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = f"apt_data_{current_datetime}.csv"
df.to_csv(csv_filename, index=False)
print(f"Data saved to {csv_filename}")