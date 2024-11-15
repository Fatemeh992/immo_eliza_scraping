
"""from bs4 import BeautifulSoup
import json
import re
from selenium import webdriver


driver = webdriver.Chrome() 
driver.get("https://www.immoweb.be/en/classified/house/for-sale/wetteren/9230/20316344")
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()
list_data=''
list_pattern = re.compile(r'av_items\s*=\s*(\[\{.*?\}\])', re.DOTALL)
script_tags = soup.find_all("script")
for script in script_tags:
    script_content = script.string or script.get_text() 
    if script_content:
        match = list_pattern.search(script_content)
        if match:
            print("Yes")
            list_data = match.group(0) 
            print("List found in script tag:")
            print(list_data)
            print(type(list_data))
            
        

list_data = re.sub(r'^.*?=\s*', '', list_data, flags=re.DOTALL).strip()
list_data = re.sub(r'(\s|{|,)(\w+):', r'\1"\2":', list_data)
list_data = list_data.replace('GA4Context', '"GA4Context"')
list_data = list_data.replace(": true", ": true").replace(": false", ": false")
list_data= re.sub(r',\s*([\]}])', r'\1', list_data)

try:
    parsed_data = json.loads(list_data)
    print("Parsed JSON Data:", parsed_data)
    print(type(parsed_data))
except json.JSONDecodeError as e:
    print("JSON decoding failed:", e)
    print("Revised list_data:", list_data) """


import requests
from bs4 import BeautifulSoup
import json

def get_property_details(property_url):
    details_list={}
    
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"})
    if response.status_code == 200:
        soup= BeautifulSoup(response.content, 'html.parser')
        s = soup.select('iw-load-advertisements')
        if len(s) > 0:
            data = json.loads(s[0].attrs[":classified"])
            Bedrooms = data["property"]["bedroomCount"]
            property_type = data["property"]["type"]
            property_type = data["property"]["subtype"]
            Locality = data["property"]["location"]["locality"]
            Kitchen = data["property"]["kitchen"]["type"]
            Facades = data["property"]["building"]["facadeCount"]
            Price = data["transaction"]["sale"]["price"]
            Furnished = data["transaction"]["sale"]["isFurnished"]
            Terrace = data["property"]["hasTerrace"]
            TerraceSurface = data["property"]["terraceSurface"]
            Fireplace = data["property"]["fireplaceExists"]


get_property_details("https://www.immoweb.be/en/classified/apartment/for-sale/uccle/1180/20315652")

