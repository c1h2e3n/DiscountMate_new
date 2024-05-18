import time
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


from bs4 import BeautifulSoup

# Retrieve configuration values
config = configparser.ConfigParser()
config.read('configuration.ini')

delay = int(config.get('Coles', 'DelaySeconds'))
ccsuburb = str(config.get('Coles', 'ClickAndCollectSuburb'))
category_ignore = str(config.get('Coles', 'IgnoredCategories'))

# Configure options
options = webdriver.EdgeOptions()
options.add_argument("--app=https://www.coles.com.au")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Start EdgeDriver
print("Starting Coles...")
driver = webdriver.Edge(options=options)

# Navigate to the Coles website
url = "https://www.coles.com.au"
driver.get(url + "/browse")
time.sleep(delay)
 
try:
    # Wait for the element to be clickable
    element = WebDriverWait(driver, 180).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='delivery-selector-button']"))
    )

    # If element found, proceed with the click
    element.click()
    # Wait for the element to be clickable
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='delivery-selector-button']")))
    
    # Set Location via Menu Items
    driver.find_element(By.XPATH, "//button[@data-testid='delivery-selector-button']").click()
    time.sleep(delay)

    driver.find_element(By.XPATH, "//a[@id='shopping-method-label-0']").click()
    time.sleep(delay)

    driver.find_element(By.XPATH, "//input[@aria-label='Search address']").send_keys(ccsuburb)
    time.sleep(delay)

    driver.find_element(By.XPATH, "//div[@id='react-select-search-location-box-option-0']").click()
    time.sleep(delay)

    driver.find_element(By.XPATH, "//input[@name='radio-group-name'][@value='0']").click()
    time.sleep(delay)

    driver.find_element(By.XPATH, "//button[@data-testid='set-location-button']").click()
    time.sleep(delay)

except TimeoutException:
    print("Setting C+C Location Failed: Timed out waiting for element to be clickable")
except Exception as e:
    print("Setting C+C Location Failed:", str(e))  # Print the error message

 
# Parse the page content
page_contents = BeautifulSoup(driver.page_source, "html.parser")

# Find all product categories on the page
categories = page_contents.find_all("a", class_="coles-targeting-ShopCategoriesShopCategoryStyledCategoryContainer")

# Remove categories ignored in the config file
categories_to_scrape = []
for category in categories:
    category_endpoint = category.get("href").replace("/browse/", "").replace("/", "")
    if category_endpoint not in category_ignore:
        categories_to_scrape.append(category.text)

# Iterate through each category and follow the link to get the products
products_data = []
output_count = 0  # Counter for number of outputs
max_outputs = 10  # Maximum number of outputs
for category_name in categories_to_scrape:
    # Get the link to the category page
    category_link = f"{url}/{category_name}"
    
    print("Loading Category:", category_name)

    # Follow the link to the category page
    driver.get(category_link)

    # Parse page content
    page_contents = BeautifulSoup(driver.page_source, "html.parser")

    # Get all products on the page
    products = page_contents.find_all("header", class_="product__header")

    # Iterate through each product and extract the product data
    for product in products:
        # Increment the output count
        output_count += 1

        # Check if the maximum number of outputs has been reached
        if output_count > max_outputs:
            break

        name = product.find("h2", class_="product__title")
        itemprice = product.find("span", class_="price__value")
        unitprice = product.find("div", class_="price__calculation_method")
        specialtext = product.find("span", class_="roundel-text")
        complexpromo = product.find("span", class_="product_promotion complex")
        productLink = product.find("a", class_="product__link")["href"]
        productcode = productLink.split("-")[-1]
        price_was = None

        if name and itemprice:
            product_data = {
                "Product Code": productcode,
                "Category": category_name,
                "Item Name": name.text.strip(),
                "Best Price": itemprice.text.strip(),
                # Add other fields as needed
            }
            products_data.append(product_data)

    # Check if the maximum number of outputs has been reached
    if output_count > max_outputs:
        break

# Close the browser
driver.quit()

# Print the scraped data
for product_data in products_data:
    print(product_data)

print("Finished")
