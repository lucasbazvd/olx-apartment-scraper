import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

pages = 21

for i in range(1, pages):
    # Obtendo o HTML
    url = f'https://www.zapimoveis.com.br/aluguel/apartamentos/pr+curitiba/?__ab=sup-hl-pl:newC,exp-aa-test:B,super-high:new,olx:control,phone-page:new,off-no-hl:new,zapcopsmig:control&transacao=aluguel&onde=,Paran%C3%A1,Curitiba,,,,,city,BR%3EParana%3ENULL%3ECuritiba,-25.437238,-49.269973,&tipos=apartamento_residencial&pagina={str(i)}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        html = response.text
        
        soup = BeautifulSoup(html, 'html.parser')
        apartment_divs = soup.find_all("div", {"class": "ListingCard_result-card__Pumtx"})
        
        apts = []

        for i in apartment_divs:
            div_1 = i.find("div", {"class": "ListingCard_header__wrapper__sI7ZX"})
            if div_1:
                section_1 = div_1.find("section")
                if section_1:
                    div_2 = section_1.find("div")
                    if div_2:
                        title_h2 = div_2.find("h2")
                        if title_h2:
                            print(title_h2.text)
                            apts.append(title_h2.text)
        
        print(len(apts))
    else:
        print(f"Failed to retrieve page {i}: {response.status_code}")
    
    time.sleep(2)  # Pause for 2 seconds before the next request
