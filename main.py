import requests
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd

chrome_driver = 'C:\chromedriver.exe' # put the path to the chromedriver here
driver = webdriver.Chrome(chrome_driver)

# login do strony
url = "url"
s = requests.Session()
r = s.get(url)
data = {
    'login': 'l',
    'password': 'T'}

requests.post(url,data=data)

d = s.post(url, data=data, headers=dict(Referer=url))

# idziemy do katalogu
driver.get("https://www.b2b-spaw.pl/ProductsCatalog/Index?setFavoriteProducts=true")

# ciekamy na ładowania strony i szukamy potrzebną klasę 'headNameSpan' , gdzie mamy nazwę
wait = WebDriverWait(driver, 100)

#szuka element z nazwą headNameSpan
element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'headNameSpan')))

#pobieraz source_page
html = driver.page_source

#i nareście rozbieramy strone na części przy pomocy soup
soup = BeautifulSoup(html, 'html.parser')


#tworzymy listę, w której będziemy zachować nazwy produktów
name_list = []
for name in soup.find_all('span', {'class': 'headNameSpan'}):
    name_list.append(name.get_text())

#Tu kolejna lista dla SKU
all_catalog_list = []
all_catalog = soup.find_all('span', {'class': 'text'})

#wyciągamy każdy drugi element, ponieważ na b2b mamy jedną klassę dla dwóch elementów
for i, catalog in enumerate(all_catalog):
    if i % 2 == 0:
        all_catalog_list.append(catalog.text)


#Kolejna lista dla dostępności
availability_list = []
availability = soup.find_all('span', {'class': ['text productDetailAvailability availability_ONE_DAY whiteSpaceNowrap', "availability_PHONE"]})
for avail in availability:
    availability_list.append(avail.text)



#tworzymy excel z 3 kołumnami i dodajemy listy z danymi pojedynczo do każdej
df = pd.DataFrame(columns=['Name', 'Catalog', 'Availability'])
for name, catalog, availability in zip(name_list, all_catalog_list, availability_list):
    df = df.append({'Name': name, 'Catalog': catalog, 'Availability': availability}, ignore_index=True)

#zapisujemy do excel
df.to_excel('outputiiiiiss.xlsx', index=False)



