import requests
import time
from bs4 import BeautifulSoup
import json
import os

property_links = []
start_page = 1
if os.path.exists('state.json'):
    with open('state.json', 'r') as file:
        state = json.load(file)
        property_links = state["property_links"]
        start_page = state["page"]

for page in range(start_page, 334):
    url = f'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false&page={page}&orderBy=relevance'
    #url = f'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page={page}&orderBy=relevance'

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"})
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html')
        
        links = soup.select('article.card.card--result div.card--result__body a.card__title-link')
        if len(links) > 0 :
            for link in links:
                property_links.append(link.attrs["href"])
        else:
            print("error on page", page)
            state = {"page": page, "property_links":property_links}
            with open('state.json', 'w') as file:
                json.dump(state, file)
            break    
        time.sleep(2)
    else:
        print("error on page", page)
        state = {"page": page, "property_links":property_links}
        with open('state.json', 'w') as file:
            json.dump(state, file)
        break
