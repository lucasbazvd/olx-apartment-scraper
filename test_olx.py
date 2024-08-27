from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument("--log-level=1")
chrome_options.add_argument("--disable-web-security")

driver = webdriver.Chrome(options=chrome_options)

pages = 70

def scroll_slowly(driver):
    total_height = driver.execute_script("return document.body.scrollHeight")
    scrolled = 0
    while scrolled < total_height:
        scroll_amount = random.randint(250, 500)
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        scrolled += scroll_amount
        time.sleep(random.uniform(0.5, 1.5))
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height > total_height:
            total_height = new_height
        print(f"Scrolled: {scrolled}/{total_height} pixels")


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
            
            # Extract IPTU and Condomínio
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


for i in range(1, pages):
    url = f"https://www.olx.com.br/imoveis/aluguel/apartamentos/estado-pr/regiao-de-curitiba-e-paranagua?o={i}"
    driver.get(url)
    
    print(f"\nProcessing page {i}")
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "section.olx-ad-card.olx-ad-card--horizontal"))
    )

    scroll_slowly(driver)

    apartments = get_apartment_data(driver)
    
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

    pause_time = random.uniform(2.0, 4.0)
    print(f"\nPausing for {pause_time:.2f} seconds before next page")
    time.sleep(pause_time)

driver.quit()