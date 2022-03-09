from os import environ
import os
import time
from unshortenit import UnshortenIt
from urllib.request import urlopen
from urllib.parse import urlparse
import aiohttp
from pyrogram import Client, filters
from pyshorteners import Shortener
from bs4 import BeautifulSoup
import requests
import re

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
BOT_TOKEN = environ.get('BOT_TOKEN')
API_KEY = environ.get('API_KEY')
CHANNEL = environ.get('CHANNEL')
HOWTO = environ.get('HOWTO')

bot = Client('Droplink bot', 
             api_id=API_ID, 
             api_hash=API_HASH,
             bot_token=BOT_TOKEN)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hi {message.chat.first_name}!**\n\n"
        "**I'm Powerful Web-Dl Bot \nCreated BY @Professional_Seller200 🧑‍💻 \n\n Here I support MPD Links & \nDirect DRM links of Zee5, Voot, Sunnxt, Namma Flix, AltBalaji, Hoichoi, Aha, Sonyliv, SparkOTT, AMAZON Prime, PrimeVideo, Mxplayer, Hotstar, Shemaroome, Jio-Cinema, NF(on the way).......\n\nHit /Help to Know More About Me 🤖 \n** ")

@bot.on_message(filters.command('help') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**{message.chat.first_name}!**\n\n"
        "**Avilable Commands 👇🏻\nFor Voot DRM Video Download use /Voot \nFor Hotstar DRM Video Download Use /Hoststar \nFor zee5 DRM Videos Download use /zee5 \nSunnext DRM Videos Download /Sunnext \nContact Bot Support Team Use /support \n IF you Wants to know Prize Hit /plans \n\nIF Want To Buy Subscription Contact @Professional_Seller200🔐**")

@bot.on_message(filters.command('Sunnext') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**{message.chat.first_name}!**\n"
        "**Please send Your Sunnext Link. . . .**")

@bot.on_message(filters.command('Hotstar') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**{message.chat.first_name}!**\n"
        "**Please send Your Hotstar Link. . . .**")

@bot.on_message(filters.command('Voot') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hey, {message.chat.first_name}!**\n"
        "**Please Send Your voot link. . .**")

@bot.on_message(filters.command('support') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**{message.chat.first_name}!**\n"
        "**If You Wants To Buy Subscription Of This Bot\n Contact @Professional_Seller200 🧑‍💻**")

@bot.on_message(filters.command('Zee5') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**{message.chat.first_name}!**\n"
        "**please Send Your Zee5 Link. . .**")

@bot.on_message(filters.command('plans') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**{message.chat.first_name}!**\n"
        "**Prize Not Fixed Yet Fixed Soon 😌👍🏻**")
    
@bot.on_message(filters.text & filters.private)
async def pdisk_uploader(bot, message):
    new_string = str(message.text)
    conv = await message.reply("Prosessing Your Link. . .")
    dele = conv["message_id"]
    try:
        pdisk_link = await multi_pdisk_up(new_string)
        await bot.delete_messages(chat_id=message.chat.id, message_ids=dele)
        await message.reply(f'{pdisk_link}' , quote=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


@bot.on_message(filters.photo & filters.private)
async def pdisk_uploader(bot, message):
    new_string = str(message.caption)
    conv = await message.reply("Prosessing Your Link...")
    dele = conv["message_id"]
    try:
        pdisk_link = await multi_pdisk_up(new_string)
        if(len(pdisk_link) > 1020):
            await bot.delete_messages(chat_id=message.chat.id, message_ids=dele)
            await message.reply(f'{pdisk_link}' , quote=True)
        else:
            await bot.delete_messages(chat_id=message.chat.id, message_ids=dele)
            await bot.send_photo(message.chat.id, message.photo.file_id, caption=f'{pdisk_link}')
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)
    
async def pdisk_up(link):
    if ('mega' in link or 'google' in link or 'mdisk' in link or 'entertainvideo' in link or 'dood' in link or 'bit' in link ):
        url = 'https://droplink.co/api'
        params = {'api': API_KEY, 'url': link}
    
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, raise_for_status=True) as response:
                data = await response.json()
                v_url = """You are not a authorized User 🙄 \nGet Access From @Professional_Seller200 ⚡"""
             
    else:
        v_url = link
        
    return ("""You are not a authorized User 🙄 \nGet Access From @Professional_Seller200 ⚡"""

             )

async def multi_pdisk_up(ml_string):
    list_string = ml_string.splitlines()
    ml_string = ' \n'.join(list_string)
    new_ml_string = list(map(str, ml_string.split(" ")))
    new_ml_string = await remove_username(new_ml_string)
    new_join_str = "".join(new_ml_string)

    urls = re.findall(r'(https?://[^\s]+)', new_join_str)

    nml_len = len(new_ml_string)
    u_len = len(urls)
    url_index = []
    count = 0
    for i in range(nml_len):
        for j in range(u_len):
            if (urls[j] in new_ml_string[i]):
                url_index.append(count)
        count += 1
    new_urls = await new_pdisk_url(urls)
    url_index = list(dict.fromkeys(url_index))
    i = 0
    for j in url_index:
        new_ml_string[j] = new_ml_string[j].replace(urls[i], new_urls[i])
        i += 1

    new_string = " ".join(new_ml_string)
    return await addFooter(new_string)

async def new_pdisk_url(urls):
    new_urls = []
    for i in urls:
        time.sleep(0.2)
        new_urls.append(await pdisk_up(i))
    return new_urls  

async def remove_username(new_List):
    for i in new_List:
        if('@' in i or 't.me' in i or 'https://bit.ly/abcd' in i or 'https://bit.ly/123abcd' in i or 'telegra.ph' in i):
            new_List.remove(i)
    return new_List
  
        
bot.run()
mi
