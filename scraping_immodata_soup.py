""import requests
from bs4 import BeautifulSoup
import pandas
import time

data_url="https://www.immoweb.be/en"
cookies=requests.get(data_url).cookies
response=requests.get(data_url,parse='html-parse',cookies=cookies)

if response.status_code == 200 :






driver.execute_script("document.getElementById('usercentrics-root').style.display = 'none';")

"""search_button = driver.find_element(By.XPATH, "//button[@id='searchBoxSubmitButton']")
search_button.click()"""

search_list=driver.find_elements(By.XPATH, '//div[@class="search-results"]/ul[@class="search-results__list"]/div/li[@class="search-results__item"]')
print(f"InTotal :{len(search_list)}")
#data=[]
property_links=[]
#life_annuity_text=[]
for row in search_list:

    driver.execute_script("document.getElementById('usercentrics-root').style.display = 'none';")
    time.sleep(2)
    property_link = row.find_element(By.XPATH, "//a[@class='card__title-link']")
    property_links.append(property_link.get_attribute('href'))
    property_link.click()
    life_annuity=driver.find_element(By.XPATH,"//div[@class='classified-gallery__item']/div[@class='flag-list container']/div[@class='flag-list__item flag-list__item--secondary']/span[@class='flag-list__text']")
    #time.sleep()
    print(life_annuity.text)
    break
    details= driver.find_elements(By.XPATH,"//div[@class='container container--body']/div[@class='text-block']")
    for row in details:
        all_sections = row.find_elements(By.XPATH,"//table[@class='classified-table']")
        print(f"categories: {len(all_sections)}")
        for x in all_sections:
            allrows = x.find_elements(By.XPATH, "//tr")
            print(f"rows in each category: {len(allrows)}")

print(len(property_links))
print(property_links)   
    
#driver.quit()""



import requests
import time
from bs4 import BeautifulSoup

property_links = []
for page in range(1, 334):
    url = f'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page={page}&orderBy=relevance'

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"})
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html')

        for res in soup.select('article.card.card--result div.card--resultbody a.cardtitle-link'):
            property_links.append(res.attrs["href"])
        time.sleep(2)
    else:
        print("error on page", page)
        break


