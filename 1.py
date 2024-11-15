
from bs4 import BeautifulSoup
import json
import re
from selenium import webdriver


driver = webdriver.Chrome() 
driver.get("https://www.immoweb.be/en/classified/apartment/for-sale/uccle/1180/20315652")
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()
list_pattern = re.compile(r'av_items\s*=\s*(\[\{.*?\}\])', re.DOTALL)
script_tags = soup.find_all("script")
for script in script_tags:
    script_content = script.string or script.get_text() 
    if script_content:
        match = list_pattern.search(script_content)
        if match:
            list_data = match.group(0) 
            print("List found in script tag:")
            print(list_data)
            
        
# Step 1: Remove the variable declaration (everything before the first `[`)
list_data = re.sub(r'^.*?=\s*', '', list_data, flags=re.DOTALL).strip()

# Step 2: Add quotes around any unquoted keys or values
# Convert unquoted keys to quoted keys
list_data = re.sub(r'(\s|{|,)(\w+):', r'\1"\2":', list_data)


# Step 3: Specifically handle variables like GA4Context and replace them with string literals
# We will replace GA4Context with a placeholder string (assuming it's a string)
list_data = list_data.replace('GA4Context', '"GA4Context"')


# Step 4: Replace JavaScript true/false with JSON-compatible true/false
list_data = list_data.replace(": true", ": true").replace(": false", ": false")
list_data= re.sub(r',\s*([\]}])', r'\1', list_data)

# Step 5: Try parsing as JSON
try:
    parsed_data = json.loads(list_data)
    print("Parsed JSON Data:", parsed_data)
    print(type(parsed_data))
except json.JSONDecodeError as e:
    print("JSON decoding failed:", e)
    print("Revised list_data:", list_data) 

