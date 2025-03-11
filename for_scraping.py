import requests
from bs4 import BeautifulSoup
import re

"""
The following section is to get the property HTML and then dissect the attributes.
"""
def get_property(url):
    #This fetches the content of the site.
    property = requests.get(url).content
    return property

def get_address(results):
    #This is used to get the address.
    address = results.find_all("div", class_ = "font-bold text-sm md:text-base").pop().text
    return address

def get_zip_code(results):
    #This is used to get the zip-code.
    zip_code = results.find_all("div", class_ = "mt-1 text-xs md:text-sm text-gray-600").pop().text
    return zip_code

def get_price_year(results):
    #This is used to get the price.
    price_year = results.find_all("div", class_ = "text-gray-600")[1].text
    RegEx_price = r'(?<=: ).*(?= kr)'
    RegEx_year = r'(?<=\()\d*(?=\))'
    price = re.findall(RegEx_price, price_year).pop().replace(".","")
    year = re.findall(RegEx_year, price_year).pop()
    return float(price), int(year)

def get_size_rooms_toilets(results):
    #This is used to get the size, no. of rooms and toilets of the property.
    size, rooms, toilets = results.find_all("div", class_ = "flex flex-row select-none mt-2")
    pattern = r'^\d*'
    size, rooms, toilets = int(re.findall(pattern, size.text).pop()), int(re.findall(pattern, rooms.text).pop()), int(re.findall(pattern, toilets.text).pop())
    return size, rooms, toilets

def convert_type(type):
    types = {
        'normal': 'Fri handel',
        'auction': 'Auktion',
        'family': 'Familiehandel'
    }
    return types[type]

def treat_property(property,type):
    #This is to deliver the final results as a dictionary.
    read_html = BeautifulSoup(property, "html.parser")
    results = read_html.find_all("div", class_="scroll-mt-0").pop()
    size, rooms, toilets = get_size_rooms_toilets(results)
    price, year = get_price_year(results)
    property = {
        'Adresse': get_address(results),
        'Post nr.': get_zip_code(results),
        'Pris': price,
        'År': year,
        'Størrelse (m2)': size,
        'Værelser': rooms,
        'Toiletter': toilets,
        'Handel': convert_type(type)
    }
    return property

#url = 'https://www.boligsiden.dk/adresse/prinsesse-maries-alle-1-1-5000-odense-c-04616272___1__1____'
#results = treat_property(get_property(url))
#print(results)

"""
The following section is for finding the appropriate links for the properties
from the main page.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--start-maximized")
import time
def get_links(url):
    #Gets the links on the current page.
    links = []
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    time.sleep(2)
    properties = browser.page_source
    browser.close()
    properties = BeautifulSoup(properties, 'html.parser')
    properties = properties.find_all('div', class_='shadow overflow-hidden mx-4')
    for property in properties:
        link = property.find_all('a', href=True).pop()
        links.append('https://www.boligsiden.dk'+link['href'])
    return links

with_page = lambda n, type: f"https://www.boligsiden.dk/kommune/odense/solgte/alle?sortAscending=false&yearSoldFrom=2020&mapBounds=10.173702,55.284897,10.582207,55.48396&registrationTypes={type}&latestRegistrationType={type}&sortBy=soldDate&page={n}"
#url = with_page(1,'normal')
#print(url)
#print(get_links(url))
