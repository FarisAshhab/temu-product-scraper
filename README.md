# Temu Product Scraper

This project is a web scraping tool that extracts product data from the Temu website and displays it using a Flask web application.

## Features
- Manual login to Temu to handle CAPTCHA
- Scrapes product name, price, rating, and image URL
- Displays data on a modern web interface
- Search functionality to filter products by name and price range

## Requirements
- Python 3.x
- Google Chrome browser
- ChromeDriver corresponding to your Chrome version

## Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/farisashhab/temu-product-scraper.git
cd WebScraper


Step 2: Install Python Dependencies
pip install -r requirements.txt


Step 3: Download ChromeDriver
Download the ChromeDriver that matches your version of Chrome from here: https://developer.chrome.com/docs/chromedriver/downloads
Extract the downloaded file and place it in the WebScraper directory.

Step 4: Run the Flask Application
python app.py

Open a web browser and navigate to http://127.0.0.1:5000.

Step 5: Usage
Click "Login to Temu" and manually log in to the Temu website.
Click "Scrape Summer Sale Products" to start scraping the product data.
Use the search functionality to filter the displayed products.
Project Structure
app.py: Flask web application
scrape.py: Selenium script for web scraping
static/: Directory for static files (e.g., images, CSS)
templates/: Directory for HTML templates
requirements.txt: Python dependencies
.gitignore: Git ignore file
README.md: Project instructions and documentation


License
This project is licensed under the MIT License.

