import time
import logging
from telegram import Bot
from telegram.ext import Updater
import requests
from concurrent.futures import ThreadPoolExecutor

TOKEN = '6708110180:AAH0UxHXimsHtX15xexZGHdN8_oKrHmn7Z0'
CHAT_ID = '907855315'
KEYWORD_DETECTED = False

# List of product sites
product_sites = [
    {'url': 'https://www.dzrt.com/en/icy-rush.html', 'name': 'ICY RUSH'},
    {'url': 'https://www.dzrt.com/en/highland-berries.html', 'name': 'HIGHLAND BERRIES'},
    {'url': 'https://www.dzrt.com/en/mint-fusion.html', 'name': 'MINT FUSION'},
    {'url': 'https://www.dzrt.com/en/spicy-zest.html', 'name': 'SPICY ZEST'},
    {'url': 'https://www.dzrt.com/en/garden-mint.html', 'name': 'GARDEN MINT'},
    {'url': 'https://www.dzrt.com/en/purple-mist.html', 'name': 'PURPLE MIST'},
    {'url': 'https://www.dzrt.com/en/seaside-frost.html', 'name': 'SEASIDE FROST'},
    {'url': 'https://www.dzrt.com/en/edgy-mint.html', 'name': 'EDGY MINT'},
    
    # Limited Edition
#    {'url': 'https://www.dzrt.com/en/samra.html', 'name': 'SAMRA'},
#    {'url': 'https://www.dzrt.com/en/tamra.html', 'name': 'TAMRA'},
#    {'url': 'https://www.dzrt.com/en/haila.html', 'name': 'HAILA'},

]
bot = Bot(token=TOKEN)
# Create a session object
session = requests.Session()
session.mount('http://', requests.adapters.HTTPAdapter(pool_connections=1000, pool_maxsize=1000))
session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=1000, pool_maxsize=1000))

# Function to check if the site has changed
def check_site_change(url, keyword):
    global KEYWORD_DETECTED
    previous_content = get_previous_content(url)
    response = session.get(url)
    current_content = response.text
    if previous_content != current_content:
        if keyword not in current_content and not KEYWORD_DETECTED:
            send_notification(url, keyword, ">", product_sites)
            KEYWORD_DETECTED = True
            logging.info(f"Keyword '{keyword}' not found on the page. Sending notification.")
        else:
            logging.info(f"Keyword '{keyword}' found on the page. No notification sent.")
    else:
        logging.info("Page content has not changed.")
    KEYWORD_DETECTED = False

# Function to get the previous content of the site
def get_previous_content(url):
    try:
        response = session.get(url)
        return response.text
    except requests.exceptions.RequestException:
        return None

# Function to send notification
def send_notification(url, keyword, message, product_sites):
    global KEYWORD_DETECTED
    chat_id = CHAT_ID
    matching_products = [product for product in product_sites if product['url'] == url]
    for product in matching_products:
        product_name = product['name']
        bot.send_message(
            chat_id=chat_id,
            text=f"{message} {product_name} {url} متوفر الان ",
            parse_mode='HTML'
        )
    KEYWORD_DETECTED = False

# Start checking each product site for the target keyword
keyword = 'Back In Stock Soon'
while True:
    with ThreadPoolExecutor(max_workers=len(product_sites)) as executor:
        futures = [executor.submit(check_site_change, product_site['url'], keyword) for product_site in product_sites]
    time.sleep(0)  # Wait for 3 seconds before checking the next site