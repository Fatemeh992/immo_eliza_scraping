import requests
import time
import csv
from bs4 import BeautifulSoup
from threading import Thread
from time import perf_counter

property_links = []


def fetch_links(page):
    url = f'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false&page={page}&orderBy=relevance'
    start_time = perf_counter()
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"})
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        for res in soup.select('article.card.card--result div.card--result__body a.card__title-link'):
            property_links.append(res.attrs["href"])
        duration = perf_counter() - start_time
        print(f"Page {page} fetched in {duration:.4f} seconds.")
    else:
        print(f"Error on page {page}")


program_start = perf_counter()


threads = []
for page in range(1, 334):
    thread = Thread(target=fetch_links, args=(page,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()


program_duration = perf_counter() - program_start
print(f"\nTotal time taken for program: {program_duration:.4f} seconds.")
print(property_links)

with open('property_links.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for url in property_links:
        writer.writerow([url])
