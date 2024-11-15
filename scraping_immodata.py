import requests
from bs4 import BeautifulSoup
import pandas
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from threading import Thread
from time import perf_counter

property_links=[]
def fetch_links(page):
    data_url=f"https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&isALifeAnnuitySale=false&page={page}&orderBy=relevance"
    start_time = perf_counter()
    driver = webdriver.Chrome()
    driver.get(data_url)
    wait = WebDriverWait(driver, 10)

    """try:
        
        cookie_button = driver.find_element(By.XPATH, "//button[contains(text(),'OK')]")
        cookie_button.click()
        shadow_root = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "usercentrics-root"))).shadow_root
        button = WebDriverWait(shadow_root, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid=uc-accept-all-button]")))
        time.sleep(5)
        if button:
            button.click()

    except:
        print("Cookie consent button not found or already accepted.")"""


    driver.execute_script("document.getElementById('usercentrics-root').style.display = 'none';")
    search_button = driver.find_element(By.XPATH, "//button[@id='searchBoxSubmitButton']")
    search_button.click()
    time.sleep(2)
    search_list=driver.find_elements(By.XPATH, '//div[@class="search-results"]/ul[@class="search-results__list"]/div/li[@class="search-results__item"]')
    #print(f"InTotal :{len(search_list)}")
   
    for row in search_list:
        property_link = driver.find_element((By.XPATH, "//a[@class='card__title-link']"))
        driver.quit()
        property_links.append(property_link.get_attribute('href'))
            
    duration = perf_counter() - start_time
    print(f"Page {page} fetched in {duration:.4f} seconds.")


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
print(len(property_links))
print(f"\nTotal time taken for program: {program_duration:.4f} seconds.")




