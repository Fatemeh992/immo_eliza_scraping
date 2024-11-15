import requests
from bs4 import BeautifulSoup
import json
from typing import Any

def get_in(data: dict, keys: list, default: Any = None):
    obj = data
    for key in keys:
        if not obj or key not in obj:
            return default
        obj = obj[key]
    return obj

def getTypeOfSale(data):
    keys = ["isPublicSale", "isNotarySale", "isLifeAnnuitySale", "isAnInteractiveSale", "isNewlyBuilt", "isInvestmentProject", "isUnderOption", "isNewRealEstateProject"]
    for key in keys:
        if get_in(data, ["flags", key]) == True:
            return key.replace("is", "")

url = 'https://www.immoweb.be/en/classified/apartment/for-sale/ninove/9400/20318192'
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"})
if response.status_code == 200:
    soup= BeautifulSoup(response.content, 'html.parser')

    parsed_data = {}
    s = soup.select('iw-load-advertisements')

    if len(s) > 0 and s[0].has_attr(":classified"):
        data = json.loads(s[0].attrs[":classified"])

        parsed_data["bedrooms"] = get_in(data, ["property", "bedroomCount"])
        parsed_data["property_type"] = get_in(data, ["property", "type"])
        parsed_data["property_subtype"] = get_in(data, ["property", "subtype"])
        parsed_data["locality"] = get_in(data, ["property", "location", "locality"])
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
        parsed_data["landSurface"] = get_in(data, ["property","land", "surface"])
        parsed_data["livingArea"] = get_in(data, ["property", "netHabitableSurface"])
        parsed_data["surfaceOfThePlot"] = get_in(data, ["property","land", "surface"])
        parsed_data["typeOfSale"] = getTypeOfSale(data)
        

    print(parsed_data)

    