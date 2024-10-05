import asyncio
import js2py
import requests
import os, sys, ssl
from telethon.sync import TelegramClient
from telethon import events
from telethon.sync import functions, types, events
from urllib.parse import unquote
import aiocron
import base64
import random
import time
import json
from threading import Thread, active_count
from concurrent.futures import ThreadPoolExecutor
from telethon.extensions import markdown, html
from telethon import types


# -----------
class CustomMarkdown:
    @staticmethod
    def parse(text):
        text, entities = html.parse(text)
        for i, e in enumerate(entities):
            if isinstance(e, types.MessageEntityTextUrl):
                if e.url == 'spoiler':
                    entities[i] = types.MessageEntitySpoiler(e.offset, e.length)
                elif e.url.startswith('emoji/'):
                    entities[i] = types.MessageEntityCustomEmoji(e.offset, e.length, int(e.url.split('/')[1]))
        return text, entities
    @staticmethod
    def unparse(text, entities):
        for i, e in enumerate(entities or []):
            if isinstance(e, types.MessageEntityCustomEmoji):
                entities[i] = types.MessageEntityTextUrl(e.offset, e.length, f'emoji/{e.document_id}')
            if isinstance(e, types.MessageEntitySpoiler):
                entities[i] = types.MessageEntityTextUrl(e.offset, e.length, 'spoiler')
        return html.unparse(text, entities)
with open('config.json') as f:
    data = json.load(f)
    api_id = data['api_id']
    api_hash = data['api_hash']
    admin = data['admin']

client = TelegramClient('bot', api_id, api_hash, device_model="TOM")
client.start()
client_id = client.get_me(True).user_id




print("Client is Ready ;)")
# -----------



  # Replace with your Bot Token

# app = Client("session_bot", api_id=API_ID,api_hash=API_HASH, bot_token=BOT_TOKEN)



# Replace these with your own values


CHANNEL_ID =  -1002314161300

# Initialize the Telegram client
async def fetch_tom_price():
    url = "https://api.geckoterminal.com/api/v2/networks/solana/tokens/tomDEqSDN1xdrcodffuwRDoGa8eMp7dZmS5fHGoUnvo/pools?page=1"
    previous_price = None  # Variable to store the previous price

    while True:
        response = requests.get(url)
        data = response.json()
        
        # Extract the current price of TOM
        current_price = float(data['data'][0]['attributes']['token_price_usd'])
        price_100_tom = current_price * 100
        price_10000_tom = current_price * 10000
        hour24 = data['data'][0]['attributes']['price_change_percentage']['h24']
        hour1 = data['data'][0]['attributes']['price_change_percentage']['h1']
        if hour1.startswith("-"):
            pass
        else:
            hour1 = f"+{hour24}"
      
        if hour24.startswith("-"):
            pass
        else:
            hour24 = f"+{hour24}"
      
        
        # Format the message with 8 decimal places
        message = f"<blockquote collapsible><b><u>TOKEN PRICE:</u>\n1 $TOM = ${current_price:.8f}\n100 $TOM = ${price_100_tom:.8f}\n10k $TOM = ${price_10000_tom:.8f}</b>\n\n<u><b>PRICE CHANGE PERCENTAGE</b></u>\n1h: {hour1}%\n24h: {hour24}%</blockquote collapsible>"
        
        # Calculate percentage difference if previous price exists
        if previous_price is not None:
            difference_percentage = ((current_price - previous_price) / previous_price) * 100
            
            # Only include price change in the message if it's not zero
            if difference_percentage != 0:
                message += f"\nPrice Change: {'+' if difference_percentage >= 0 else ''}{difference_percentage:.2f}%"
        
        # Update the previous price to the current price for the next iteration
        previous_price = current_price
        
        # Send the message to the specified channel
        client.parse_mode = CustomMarkdown()
        message += f"\n\n<b>TOM | The Token of 2024</b> [🍅](emoji/5924664908158341416)" 
        await client.edit_message(-1002314161300, 179, message)
        
        # Wait for 1 minute before fetching again
        await asyncio.sleep(60)

async def main():
    await fetch_tom_price()

# Run the bot
with client:
    client.loop.run_until_complete(main())
