import requests
from bs4 import BeautifulSoup
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Function to check if the site has changed
def check_site_change(url, keyword):
    previous_content = get_previous_content(url)
    response = requests.get(url)
    current_content = response.text
    if previous_content != current_content:
        send_notification(url, keyword)
    return current_content

# Function to get the previous content of the site
def get_previous_content(url):
    try:
        response = requests.get(url)
        return response.text
    except requests.exceptions.RequestException:
        return None

# Function to send notification
def send_notification(url, keyword):
    bot = Bot(token='6708110180:AAH0UxHXimsHtX15xexZGHdN8_oKrHmn7Z0')
    chat_id = '907855315'
    bot.send_message(chat_id=chat_id, text=f"Site {url} has changed. The keyword '{keyword}' has been updated.")

# Command handler for '/start' command
def start_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    url = 'https://www.dzrt.com/en/our-products.html'  # Replace with the URL of the site you want to monitor
    keyword = 'Back In Stock Soon'  # Replace with the specific word you want to monitor
    check_site_change(url, keyword)

# Function to handle errors
def error(update: Update, context: CallbackContext):
    logging.error(f'Update {update} caused error {context.error}')

# Create an updater and add handlers