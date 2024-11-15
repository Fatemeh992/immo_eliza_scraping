
import time
from threading import Thread
from time import perf_counter
import requests
from bs4 import BeautifulSoup
import json
import csv
from typing import Any
from concurrent.futures import ThreadPoolExecutor, as_completed


def fetch_links(page,property_links):
    url = f'https://www.immoweb.be/en/search/house/for-sale?countries=BE&isALifeAnnuitySale=false&isAnInvestmentProperty=false&isAPublicSale=false&isNewlyBuilt=false&maxConstructionYear=1975&minConstructionYear=1930&buildingConditions=TO_RESTORE,TO_RENOVATE,TO_BE_DONE_UP,JUST_RENOVATED&page={page}&orderBy=relevance'
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

def write_links_csv():
    with open('property_links_15Nov!4H00.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        for url in property_links:
            writer.writerow([url])


def get_in(data: dict, keys: list, default: Any = None):
    obj = data
    for key in keys:
        if not obj or key not in obj:
            return default
        obj = obj[key]
    return obj

def getTypeOfSale(data):
    keys = ["isPublicSale", "isNotarySale", "isLifeAnnuitySale", "isAnInteractiveSale", 
            "isNewlyBuilt", "isInvestmentProject", "isUnderOption", "isNewRealEstateProject"]
    for key in keys:
        if get_in(data, ["flags", key]) == True:
            return key.replace("is", "")
    return None

def get_property_data(house_index, url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"})
    parsed_data = {}
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        s = soup.select('iw-load-advertisements')
        if len(s) > 0 and s[0].has_attr(":classified"):
            data = json.loads(s[0].attrs[":classified"])

            #parsed_data["url"] = url
            parsed_data["bedrooms"] = get_in(data, ["property", "bedroomCount"])
            parsed_data["property_type"] = get_in(data, ["property", "type"])
            parsed_data["property_subtype"] = get_in(data, ["property", "subtype"])
            parsed_data["locality"] = get_in(data, ["property", "location", "locality"])
            parsed_data["postal_code"] = get_in(data, ["property", "location", "postalCode"])
            parsed_data["street"] = get_in(data, ["property", "location", "street"])
            parsed_data["number"] = get_in(data, ["property", "location", "number"])
            parsed_data["box"] = get_in(data, ["property", "location", "box"])
            parsed_data["kitchen"] = get_in(data, ["property", "kitchen", "type"])
            parsed_data["facades"] = get_in(data, ["property", "building", "facadeCount"])
            parsed_data["price"] = get_in(data, ["transaction", "sale", "price"])
            parsed_data["furnished"] = get_in(data, ["transaction", "sale", "isFurnished"])
            parsed_data["terrace"] = get_in(data, ["property", "hasTerrace"])
            parsed_data["terraceSurface"] = get_in(data, ["property", "terraceSurface"])
            parsed_data["fireplace"] = get_in(data, ["property", "fireplaceExists"])
            parsed_data["fireplaceCount"] = get_in(data, ["property", "fireplaceCount"])
            parsed_data["buildingState"] = get_in(data, ["property", "building", "condition"])
            parsed_data["garden"] = get_in(data, ["property", "hasGarden"])
            parsed_data["gardenSurface"] = get_in(data, ["property", "gardenSurface"])
            parsed_data["pool"] = get_in(data, ["property", "hasSwimmingPool"])
            parsed_data["landSurface"] = get_in(data, ["property", "land", "surface"])
            parsed_data["livingArea"] = get_in(data, ["property", "netHabitableSurface"])
            parsed_data["surfaceOfThePlot"] = get_in(data, ["property", "land", "surface"])
            parsed_data["typeOfSale"] = getTypeOfSale(data)
            
            pool = get_in(data, ["property", "hasSwimmingPool"])
            if pool:
                parsed_data["pool"] = 1
            else:
                parsed_data["pool"] = 0

            kitchen = get_in(data, ["property", "kitchen", "type"])
            if kitchen:
                parsed_data["kitchen"] = 1
            else:
                parsed_data["kitchen"] = 0

            furnished = get_in(data, ["transaction", "sale", "isFurnished"])
            if furnished:
                parsed_data["furnished"] = 1
            else :
                parsed_data["furnished"] = 0

            terrace = get_in(data, ["property", "hasTerrace"])
            if terrace:
                parsed_data["terrace"] = 1
                parsed_data["terraceSurface"] = get_in(data, ["property", "terraceSurface"])
            else:
                parsed_data["terrace"] = 0 
                parsed_data["terraceSurface"] = 0

            fireplace = get_in(data, ["property", "fireplaceExists"])
            if fireplace:
                parsed_data["fireplace"] = 1
                parsed_data["fireplaceCount"] = get_in(data, ["property", "fireplaceCount"])
            else:
                parsed_data["fireplace"] = 0 
                parsed_data["fireplaceCount"] = 0

            garden = get_in(data, ["property", "hasGarden"])
            if garden:
                parsed_data["garden"] = 1
                parsed_data["gardenSurface"] = get_in(data, ["property", "gardenSurface"])
            else:
                parsed_data["garden"] = 0
                parsed_data["gardenSurface"] = 0
    
    return house_index,parsed_data  
    

def save_property_data_2_csv(fieldnames, properties_data):
    with open("all_properties_output_15_30.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for property_data in properties_data:
            writer.writerow(property_data)

    print("CSV file created successfully.")

def main():
    program_start = perf_counter()

    property_links = []
    threads = []
    for page in range(1, 334):
        thread = Thread(target=fetch_links, args=(page,property_links))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    program_duration = perf_counter() - program_start
    print(f"\nTotal time taken for program: {program_duration:.4f} seconds.")
    write_links_csv(property_links)
    
    time.sleep(30)
    with open("property_links_15Nov!4H00.csv", "r") as links:
        urls = [(index, link.strip()) for index, link in enumerate(links)]    

    properties_data = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(get_property_data, house_index, url) for house_index, url in urls]
        for future in as_completed(futures):
            house_index ,parsed_data = future.result()  
            flattened_data = {"house_index": house_index}
            flattened_data.update(parsed_data)
            properties_data.append(flattened_data)
    fieldnames =properties_data[0].keys()
    save_property_data_2_csv(fieldnames, properties_data)

main()