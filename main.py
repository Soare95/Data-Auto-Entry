from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLScl18TCZxAEH82q_N8kEfxkKtptcTj3fUFqZH2QZIRDxa967A/viewform?usp=sf_link"
ZILLOW_WEBSITE = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B"pagination"%3A%7B%7D%2C"mapBounds"%3A%7B"west"%3A-122.8554240428207%2C"east"%3A-121.24867355453945%2C"south"%3A37.28480785882459%2C"north"%3A37.805273055221704%7D%2C"isMapVisible"%3Atrue%2C"filterState"%3A%7B"price"%3A%7B"max"%3A872627%7D%2C"beds"%3A%7B"min"%3A1%7D%2C"pmf"%3A%7B"value"%3Afalse%7D%2C"fore"%3A%7B"value"%3Afalse%7D%2C"mp"%3A%7B"max"%3A3000%7D%2C"auc"%3A%7B"value"%3Afalse%7D%2C"nc"%3A%7B"value"%3Afalse%7D%2C"fr"%3A%7B"value"%3Atrue%7D%2C"fsbo"%3A%7B"value"%3Afalse%7D%2C"cmsn"%3A%7B"value"%3Afalse%7D%2C"pf"%3A%7B"value"%3Afalse%7D%2C"fsba"%3A%7B"value"%3Afalse%7D%7D%2C"isListVisible"%3Atrue%7D'

response = requests.get(ZILLOW_WEBSITE, headers=headers)
website_response = response.text
soup = BeautifulSoup(website_response, "html.parser")

soup_href = soup.select(".list-card-top a")

zillow_links = []
for website in soup_href:
    website_link = website["href"]
    if "http" not in website_link:
        zillow_links.append(f"https://www.zillow.com{website_link}")
    else:
        zillow_links.append(website_link)

soup_prices = soup.find_all(class_="list-card-price")

zillow_prices = []
for price in soup_prices:
    text_prices = price.getText()
    text_prices = text_prices.split("/")
    last_price = text_prices[0].split("+")
    good_prices = last_price[0]
    zillow_prices.append(good_prices)

soup_addresses = soup.find_all(class_="list-card-addr")

zillow_addresses = []
for address in soup_addresses:
    street_address = address.getText()
    zillow_addresses.append(street_address)

driver = webdriver.Chrome(r"D:/chromedriver.exe")
driver.get(FORM_LINK)

for entry in range(len(zillow_addresses)):
    time.sleep(2)
    property_address = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    property_address.send_keys(zillow_addresses[entry])

    price_month = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_month.send_keys(zillow_prices[entry])

    link_property = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_property.send_keys(zillow_links[entry])

    send_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
    send_button.click()

    time.sleep(1)
    send_another = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    send_another.click()



