from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
import os

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Set path to chromedriver as per your configuration
webdriver_service = ChromeService('C:/Faris_Projects/WebScraper/chromedriver-win64/chromedriver.exe')

# URL of the Temu login page
login_url = 'https://www.temu.com/login'

# Initialize the WebDriver
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

SCRAPE_STATUS_FILE = 'scrape_status.txt'

def login():
    driver.get(login_url)
    time.sleep(5)  # Allow some time for the page to load

    # Manual login process
    print("Please manually enter your email, password, and solve the captcha.")
    print("Press the 'Continue' button on the webpage when done.")

    # Wait for the indicator file created by the frontend
    while not os.path.exists('continue.txt'):
        time.sleep(1)

    # Remove the indicator file
    os.remove('continue.txt')

    # Wait for some time to ensure the login process completes
    time.sleep(10)

def scroll_down(driver, scroll_pause_time = 1):
    # Get the initial scroll height
    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")
    
    # Set the initial position for scrolling
    current_position = 0
    new_height = 1

    while current_position < total_height:
        # Scroll down to the new position
        driver.execute_script(f"window.scrollTo({current_position}, {current_position + 500});")
        
        # Wait for the page to load
        time.sleep(scroll_pause_time)
        
        # Update the current position and the new height
        current_position += 500
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # If the new height is equal to the total height, break the loop
        if new_height == current_position:
            break
        
        total_height = new_height

def scrape_data():
    # Scroll down the page to ensure all elements are loaded
    scroll_down(driver, scroll_pause_time=2)
    
    # Wait to ensure all elements are fully loaded
    time.sleep(5)
    
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    products = []
    
    # Select product containers
    for item in soup.select('div[data-tooltip^="goodContainer-"]'):
        # Extract product name from data-tooltip-title attribute
        name = item.get('data-tooltip-title', 'No Name')
        
        # Extract price from the div with data-type="price"
        price_element = item.find('div', {'data-type': 'price'})
        price = price_element.get('aria-label', 'No Price') if price_element else 'No Price'
        
        # Extract rating if available (not mandatory as per your latest info)
        rating_element = item.find('div', class_='WCDudEtm')
        rating = rating_element.get('aria-label', 'No Rating') if rating_element else 'No Rating'
        
        # Extract image URL
        image_element = item.find('img', class_='goods-img-external')
        image_url = image_element.get('src') if image_element else 'No Image'
        
        products.append({'name': name, 'price': price, 'rating': rating, 'image_url': image_url})
    
    return products

def save_data(data):
    with open('products.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    login()
    
    # Scrape data from the default landing page after login
    data = scrape_data()
    save_data(data)
    driver.quit()

    # Update the scrape status to done
    with open(SCRAPE_STATUS_FILE, 'w') as f:
        f.write('done')

    print("Scraping completed and data saved to products.json")


