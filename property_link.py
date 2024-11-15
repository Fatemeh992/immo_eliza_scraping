import requests
import time
from bs4 import BeautifulSoup

property_links = []
for page in range(1, 334):
    url = f'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false&page={page}&orderBy=relevance'

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"})
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, features="html.parser")

        for res in soup.select('article.card.card--result div.card--result__body a.card__title-link'):
            property_links.append(res.attrs["href"])
        time.sleep(2)
    else:
        print("error on page", page)
        break

print(len(property_links))
print(property_links)