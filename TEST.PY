import requests
from bs4 import BeautifulSoup
import json
from threading import Thread, Lock
from time import perf_counter
from typing import Any

# Helper function to safely navigate nested dictionaries
def get_in(data: dict, keys: list, default: Any = None):
    obj = data
    for key in keys:
        if not obj or key not in obj:
            return default
        obj = obj[key]
    return obj

# Function to identify sale type from a given dictionary structure
def getTypeOfSale(data):
    keys = ["isPublicSale", "isNotarySale", "isLifeAnnuitySale", "isAnInteractiveSale", 
            "isNewlyBuilt", "isInvestmentProject", "isUnderOption", "isNewRealEstateProject"]
    for key in keys:
        if get_in(data, ["flags", key]) == True:
            return key.replace("is", "")

# Main function for each thread to fetch and parse property data
def get_property_data(url, house_index, houses_data_dictionary, lock):
    start_time = perf_counter()
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
            }
        )
        
        if response.status_code == 200:
            print(f"Fetched page {house_index} successfully")  # Confirm page fetch
            soup = BeautifulSoup(response.content, 'html.parser')
            s = soup.select('iw-load-advertisements')
            
            if s and s[0].has_attr(":classified"):
                try:
                    data = json.loads(s[0].attrs[":classified"])
                    
                    # Dictionary to hold parsed data for each property
                    parsed_data = {
                        "bedrooms": get_in(data, ["property", "bedroomCount"]),
                        "property_type": get_in(data, ["property", "type"]),
                        "property_subtype": get_in(data, ["property", "subtype"]),
                        "locality": get_in(data, ["property", "location", "locality"]),
                        "kitchen": get_in(data, ["property", "kitchen", "type"]),
                        "facades": get_in(data, ["property", "building", "facadeCount"]),
                        "price": get_in(data, ["transaction", "sale", "price"]),
                        "furnished": get_in(data, ["transaction", "sale", "isFurnished"]),
                        "terrace": get_in(data, ["property", "hasTerrace"]),
                        "terraceSurface": get_in(data, ["property", "terraceSurface"]),
                        "fireplace": get_in(data, ["property", "fireplaceExists"]),
                        "fireplaceCount": get_in(data, ["property", "fireplaceCount"]),
                        "buildingState": get_in(data, ["property", "building", "condition"]),
                        "garden": get_in(data, ["property", "hasGarden"]),
                        "gardenSurface": get_in(data, ["property", "gardenSurface"]),
                        "pool": get_in(data, ["property", "hasSwimmingPool"]),
                        "landSurface": get_in(data, ["property", "land", "surface"]),
                        "livingArea": get_in(data, ["property", "netHabitableSurface"]),
                        "surfaceOfThePlot": get_in(data, ["property", "land", "surface"]),
                        "typeOfSale": getTypeOfSale(data),
                    }
                    
                    # Safely update the shared dictionary with lock
                    with lock:
                        houses_data_dictionary[house_index] = parsed_data
                        print(f"Data for house {house_index} added to dictionary")
                
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error for house {house_index}: {e}")
            else:
                print(f"'iw-load-advertisements' not found or missing attribute for house {house_index}")
        else:
            print(f"Error {response.status_code} for house {house_index}, at link: {url}")
    except Exception as e:
        print(f"Error on page {house_index} at link {url}. Exception: {e}")

    duration = perf_counter() - start_time
    print(f"Thread {house_index} completed in {duration:.4f} seconds")

# Main program execution
def main(property_links):
    program_start = perf_counter()
    
    # Dictionary to hold data for all houses
    houses_data_dictionary = {}
    threads = []
    lock = Lock()  # Lock for thread-safe dictionary access

    # Launch a thread for each link in property_links
    for house_index, link in enumerate(property_links):
        thread = Thread(target=get_property_data, args=(link, house_index, houses_data_dictionary, lock))
        threads.append(thread)
        thread.start()
    
    # Join threads to ensure completion before program ends
    for thread in threads:
        thread.join()
    
    program_duration = perf_counter() - program_start
    print(f"\nTotal time taken for program: {program_duration:.4f} seconds")
    print("Final dictionary:", houses_data_dictionary)  # Final output
    print("Total houses processed:", len(houses_data_dictionary))

# Example usage
property_links = [
    # Add a list of URLs here to test
]
main(property_links)
