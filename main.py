
import time
from threading import Thread
from time import perf_counter
import requests
from bs4 import BeautifulSoup
import json
import csv
from typing import Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import pandas as pd


def fetch_links(url,page,property_links):

    url=f"{url}&page={page}"
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
    
def fetch_multiple_pages(base_url, start_page, end_page,property_links):
    # Create a list of page numbers to iterate over
    pages = list(range(start_page, end_page))
    
    # Use ThreadPoolExecutor to fetch all pages concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers based on your needs
        # Submit tasks to fetch data for each page from the base URL
        executor.map(lambda page_number: fetch_links(base_url, page_number,property_links), pages)
    

def write_links_csv(file_path,property_links):
    print("In write csv")
    with open(file_path, 'w') as csvfile:
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
    

def save_property_data_2_csv(file_path,fieldnames, properties_data):
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for property_data in properties_data:
            writer.writerow(property_data)

    print("CSV file created successfully.")

def clean_save_dataset(file_path):
    df= pd.read_csv(file_path)
    #drops duplicates
    df.drop_duplicates(subset=['postal_code','street','number','box'], inplace=True)
    #drops the empty rows if there are any.
    df.dropna(how='all',inplace=True)
    #Changing the dtype to category, better for analysis
    df['property_type']=df['property_type'].astype('category')
    df['property_subtype']=df['property_subtype'].astype('category')
    df['locality']=df['locality'].astype('category')
    df['buildingState']=df['buildingState'].astype('category')
    #replace missing values with a None
    df.map(lambda x: None if pd.isna(x) else x)
    df.to_csv("utils/cleaned_dataset.csv",index=False)

 


def main():
    program_start = perf_counter()
    property_links = []
    threads = []
    
    url1=f"https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false&isNewlyBuilt=false&minConstructionYear=1930&maxConstructionYear=1975&orderBy=relevance"
    url2=f"https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false&isNewlyBuilt=false&minConstructionYear=1976&orderBy=relevance"
    urls=[url1,url2]
    for url in urls:
        results = fetch_multiple_pages(url, 1, 334,property_links)  # Fetch pages 1 to 334
        """for page in range(1, 334):
            thread = Thread(target=fetch_links, args=(url,page,property_links))
            threads.append(thread)
            thread.start()
    for thread in threads:
        thread.join()"""
    program_duration = perf_counter() - program_start
    print(f"\nTotal time taken for program: {program_duration:.4f} seconds.")
    print(len(property_links))
    file_path = 'utils/property_links.csv'
    write_links_csv(file_path,property_links)
    
    time.sleep(30)
    with open("utils/property_links.csv", "r") as links:
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
    output_file_path="utils/all_properties_output.csv"
    save_property_data_2_csv(output_file_path,fieldnames, properties_data)
    clean_save_dataset(output_file_path)
    


if __name__ == "__main__":
    main()