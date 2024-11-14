from bs4 import BeautifulSoup
import json
import re
from selenium import webdriver
import time


driver = webdriver.Chrome() 
driver.get("https://www.immoweb.be/en/classified/house/for-sale/wetteren/9230/20316344")
time.sleep(2)
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()
list_data=''
list_pattern = re.compile(r'av_items\s*=\s*(\{.*?\});', re.DOTALL)
print(list_pattern)
script_tags = soup.find_all("script")
for script in script_tags:
    script_content = script.string or script.get_text() 
    if script_content:
        print("yes")
        match = list_pattern.search(script_content)
        print(match)
        if match:
            print("Yes")
            list_data = match.group(0) 
            print("List found in script tag:")
            print(list_data)
            print(type(list_data))



list_data = re.sub(r'^.?=\s', '', list_data, flags=re.DOTALL).strip()
list_data = re.sub(r'(\s|{|,)(\w+):', r'\1"\2":', list_data)
list_data = list_data.replace('GA4Context', '"GA4Context"')
list_data = list_data.replace(": true", ": true").replace(": false", ": false")
list_data= re.sub(r',\s([]}])', r'\1', list_data)

try:
    parsed_data = json.loads(list_data)
    print("Parsed JSON Data:", parsed_data)
    print(type(parsed_data))
except json.JSONDecodeError as e:
    print("JSON decoding failed:", e)
    print("Revised list_data:", list_data)