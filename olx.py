from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up headless Chrome
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# URL of OLX search
url = "https://www.olx.in/items/q-car-cover"
driver.get(url)

# Wait for content to load
time.sleep(5)

# Get page source and parse it
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# Extract listings
items = soup.find_all("li", {"data-aut-id": "itemBox"})
results = []

for item in items:
    title_tag = item.find("span", {"data-aut-id": "itemTitle"})
    price_tag = item.find("span", {"data-aut-id": "itemPrice"})
    location_tag = item.find("span", {"data-aut-id": "item-location"})
    
    if title_tag and price_tag:
        title = title_tag.text.strip()
        price = price_tag.text.strip()
        location = location_tag.text.strip() if location_tag else ""
        results.append({"Title": title, "Price": price, "Location": location})

# Save to CSV
df = pd.DataFrame(results)
df.to_csv("olx_car_cover_results.csv", index=False)

print("Saved OLX search results to 'olx_car_cover_results.csv'")
