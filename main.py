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

def fetch_links(url, page, property_links):
    """
    Fetches property links from a given page of the website.
    
    Args:
        url (str): The base URL for fetching properties.
        page (int): The page number to fetch.
        property_links (list): A list to store extracted property links.
    """
    url = f"{url}&page={page}"
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
    
def fetch_multiple_pages(base_url, start_page, end_page, property_links):
    """
    Fetches property links from multiple pages concurrently.
    
    Args:
        base_url (str): The base URL for fetching properties.
        start_page (int): The starting page number.
        end_page (int): The ending page number.
        property_links (list): A list to store extracted property links.
    """
    pages = list(range(start_page, end_page))
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda page_number: fetch_links(base_url, page_number, property_links), pages)

def write_links_csv(file_path, property_links):
    """
    Writes the extracted property links to a CSV file.
    
    Args:
        file_path (str): The path to save the CSV file.
        property_links (list): A list of property links.
    """
    print("In write csv")
    with open(file_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for url in property_links:
            writer.writerow([url])

def get_in(data: dict, keys: list, default: Any = None):
    """
    Retrieves a nested value from a dictionary using a list of keys.
    
    Args:
        data (dict): The input dictionary.
        keys (list): The list of keys to traverse.
        default (Any, optional): The default value if keys are not found. Defaults to None.

    Returns:
        Any: The value found at the specified keys, or the default value.
    """
    obj = data
    for key in keys:
        if not obj or key not in obj:
            return default
        obj = obj[key]
    return obj

def getTypeOfSale(data):
    """
    Determines the type of sale based on property flags.
    
    Args:
        data (dict): The property data.

    Returns:
        str: The type of sale, or None if not found.
    """
    keys = ["isPublicSale", "isNotarySale", "isLifeAnnuitySale", "isAnInteractiveSale", 
            "isNewlyBuilt", "isInvestmentProject", "isUnderOption", "isNewRealEstateProject"]
    for key in keys:
        if get_in(data, ["flags", key]) == True:
            return key.replace("is", "")
    return None

def get_property_data(house_index, url):
    """
    Fetches property details from a given URL and extracts relevant data.
    
    Args:
        house_index (int): The index of the house in the dataset.
        url (str): The property URL.

    Returns:
        tuple: The house index and a dictionary of extracted property data.
    """
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"})
    parsed_data = {}
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        s = soup.select('iw-load-advertisements')
        if len(s) > 0 and s[0].has_attr(":classified"):
            data = json.loads(s[0].attrs[":classified"])
            parsed_data["typeOfSale"] = getTypeOfSale(data)
    return house_index, parsed_data

def save_property_data_2_csv(file_path, fieldnames, properties_data):
    """
    Saves property data to a CSV file.
    
    Args:
        file_path (str): The path to save the CSV file.
        fieldnames (list): The column names for the CSV.
        properties_data (list): A list of dictionaries containing property data.
    """
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for property_data in properties_data:
            writer.writerow(property_data)
    print("CSV file created successfully.")

def clean_save_dataset(file_path):
    """
    Cleans and processes the dataset before saving.
    
    Args:
        file_path (str): The path to the dataset CSV file.
    """
    df = pd.read_csv(file_path)
    df.drop_duplicates(subset=['postal_code', 'street', 'number', 'box'], inplace=True)
    df.dropna(how='all', inplace=True)
    df.to_csv("utils/cleaned_dataset.csv", index="house_index")

def main():
    """
    Main function that orchestrates the property data scraping and processing.
    """
    program_start = perf_counter()
    property_links = []
    url1 = "https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&minConstructionYear=1930&maxConstructionYear=1975"
    url2 = "https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&minConstructionYear=1976"
    urls = [url1, url2]
    for url in urls:
        fetch_multiple_pages(url, 1, 334, property_links)
    print(len(property_links))
    file_path = 'Data/property_links.csv'
    write_links_csv(file_path, property_links)
    
    time.sleep(30)
    output_file_path = "Data/all_properties_output.csv"
    clean_save_dataset(output_file_path)

if __name__ == "__main__":
    main()
