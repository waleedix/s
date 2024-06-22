import asyncio
import aiohttp
from bs4 import BeautifulSoup
from telegram import Bot
import re

TOKEN = '6708110180:AAH0UxHXimsHtX15xexZGHdN8_oKrHmn7Z0'
CHAT_ID = '907855315'

product_sites = [
    {'url': 'https://www.dzrt.com/en/icy-rush.html', 'name': '🧊 ICY RUSH'},
    {'url': 'https://www.dzrt.com/en/highland-berries.html', 'name': '🫐 HIGHLAND BERRIES'},
    {'url': 'https://www.dzrt.com/en/mint-fusion.html', 'name': '🌿 MINT FUSION'},
    {'url': 'https://www.dzrt.com/en/spicy-zest.html', 'name': '🔥 SPICY ZEST'},
    {'url': 'https://www.dzrt.com/en/garden-mint.html', 'name': '🌿 GARDEN MINT'},
    {'url': 'https://www.dzrt.com/en/purple-mist.html', 'name': '🍇 PURPLE MIST'},
    {'url': 'https://www.dzrt.com/en/seaside-frost.html', 'name': '🌿 SEASIDE FROST'},
    {'url': 'https://www.dzrt.com/en/edgy-mint.html', 'name': '🌿 EDGY MINT'},
    
    # Limited Edition
#    {'url': 'https://www.dzrt.com/en/samra.html', 'name': 'SAMRA'},
#    {'url': 'https://www.dzrt.com/en/tamra.html', 'name': 'TAMRA'},
#    {'url': 'https://www.dzrt.com/en/haila.html', 'name': 'HAILA'},
]

product_found = False

async def check_site_for_words(url, word1_pattern, word2_pattern):
    global product_found
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            current_content = await response.text()
            soup = BeautifulSoup(current_content, 'html.parser')
            text_content = soup.get_text().lower()
            if not re.search(word1_pattern, text_content) and re.search(word2_pattern, text_content):
                send_notification(url, 'Available')
                product_found = True
                return

def send_notification(url, word):
    chat_id = CHAT_ID
    product_name = next((product['name'] for product in product_sites if product['url'] == url), 'Unknown Product')
    message = f"{product_name}                                                                 {url}                                                  Available Now ✅."
    bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode='HTML'
    )

async def scan_sites():
    global product_found
    while True:
        tasks = []
        product_found = False
        async with aiohttp.ClientSession() as session:
            for product in product_sites:
                task = asyncio.create_task(check_site_for_words(product['url'], re.compile(r'\bن\b', re.IGNORECASE), re.compile(r'\bback\s+in\s+stock\s+soon\b', re.IGNORECASE)))
                tasks.append(task)
            await asyncio.gather(*tasks)
            await asyncio.sleep(0)

            if product_found:
                await asyncio.sleep(60)
                product_found = False

bot = Bot(token=TOKEN)

async def main():
    while True:
        await scan_sites()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop