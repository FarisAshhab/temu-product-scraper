from flask import Flask, render_template, request, jsonify
import subprocess
import json
import os

app = Flask(__name__, static_folder='static')

SCRAPE_STATUS_FILE = 'scrape_status.txt'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    # Run the scrape script
    subprocess.run(['python', 'scrape.py'])

    # Read the scraped data
    with open('products.json') as f:
        products = json.load(f)
    
    return jsonify(products)

@app.route('/continue_scrape', methods=['POST'])
def continue_scrape():
    # Create the continue.txt file to signal the scrape.py script to continue
    with open('continue.txt', 'w') as f:
        f.write('continue')
    
    # Set the scrape status to running
    with open(SCRAPE_STATUS_FILE, 'w') as f:
        f.write('running')
    
    return jsonify({'status': 'continue'})

@app.route('/scrape_status', methods=['GET'])
def scrape_status():
    # Check the scrape status
    if os.path.exists(SCRAPE_STATUS_FILE):
        with open(SCRAPE_STATUS_FILE, 'r') as f:
            status = f.read().strip()
    else:
        status = 'unknown'
    
    return jsonify({'status': status})

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')

    # Read the scraped data
    with open('products.json') as f:
        products = json.load(f)

    # Filter products
    filtered_products = []
    for product in products:
        match_query = query.lower() in product['name'].lower()
        match_price = True
        if min_price:
            match_price = match_price and float(product['price'].replace('₪', '').replace(',', '')) >= float(min_price)
        if max_price:
            match_price = match_price and float(product['price'].replace('₪', '').replace(',', '')) <= float(max_price)

        if match_query and match_price:
            filtered_products.append(product)
    
    return jsonify(filtered_products)

if __name__ == '__main__':
    app.run(debug=True)


