import requests
from bs4 import BeautifulSoup
import json
import csv
from typing import Any
from concurrent.futures import ThreadPoolExecutor, as_completed

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
            parsed_data["facades"] = get_in(data, ["property", "building", "facadeCount"])
            parsed_data["price"] = get_in(data, ["transaction", "sale", "price"])
            parsed_data["landSurface"] = get_in(data, ["property", "land", "surface"])
            parsed_data["livingArea"] = get_in(data, ["property", "netHabitableSurface"])
            parsed_data["surfaceOfThePlot"] = get_in(data, ["property", "land", "surface"])
            parsed_data["typeOfSale"] = getTypeOfSale(data)
            parsed_data["buildingState"] = get_in(data, ["property", "building", "condition"])

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
            


    return house_index, parsed_data  


with open("property_links.csv", "r") as links:
    urls = [(index, link.strip()) for index, link in enumerate(links)]


properties_data = []
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(get_property_data, house_index, url) for house_index, url in urls]
    for future in as_completed(futures):
        house_index, parsed_data = future.result()  
        flattened_data = {"house_index": house_index}
        flattened_data.update(parsed_data)
        properties_data.append(flattened_data)


fieldnames = properties_data[0].keys()  

with open("all_properties_output.csv", "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for property_data in properties_data:
        writer.writerow(property_data)

print("CSV file created successfully.")
