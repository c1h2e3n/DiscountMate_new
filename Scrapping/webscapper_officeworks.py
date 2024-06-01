import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page to scrape
url = 'https://www.officeworks.com.au/shop/officeworks/c/technology/computers'

# Send a request to fetch the HTML content
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Failed to load page {url}")

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the container that holds the product information
products = soup.find_all('div', class_='product-tile')

# Lists to hold the scraped data
product_names = []
current_prices = []
full_retail_prices = []

# Loop through each product and extract the relevant information
for product in products:
    name = product.find('h2', class_='product-tile__title').text.strip()
    current_price = product.find('span', class_='product-price__price').text.strip()
    full_price = product.find('span', class_='product-price__rrp').text.strip() if product.find('span', class_='product-price__rrp') else current_price
    
    product_names.append(name)
    current_prices.append(current_price)
    full_retail_prices.append(full_price)

# Create a DataFrame from the lists
data = {
    'Product Name': product_names,
    'Current Price': current_prices,
    'Full Retail Price': full_retail_prices
}
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('officeworks_products.csv', index=False)

print('Data scraped and saved to officeworks_products.csv')
