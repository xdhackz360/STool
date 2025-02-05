import os
import logging
from pathlib import Path
from typing import Optional
import yt_dlp
import asyncio
import aiofiles
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from PIL import Image
import pytesseract
import requests
import aiohttp
from bs4 import BeautifulSoup
import json

# Path to your YouTube cookies file
YT_COOKIES_PATH = "./cookie/nm.txt"

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Function to get IP information
async def get_ip_info(ip: str) -> str:
    url = f"https://ipinfo.io/{ip}/json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return "Invalid IP address"
            data = await response.json()
    
    ip = data.get("ip", "Unknown")
    asn = data.get("org", "Unknown")
    isp = data.get("org", "Unknown")
    country = data.get("country", "Unknown")
    city = data.get("city", "Unknown")
    timezone = data.get("timezone", "Unknown")

    # Simulated IP fraud score and risk level for demonstration
    fraud_score = 0
    risk_level = "low" if fraud_score < 50 else "high"

    details = (
        f"**YOUR IP INFORMATION 🌐**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"**IP:** `{ip}`\n"
        f"**ASN:** `{asn}`\n"
        f"**ISP:** `{isp}`\n"
        f"**Country City:** `{country} {city}`\n"
        f"**Timezone:** `{timezone}`\n"
        f"**IP Fraud Score:** `{fraud_score}`\n"
        f"**Risk LEVEL:** `{risk_level} Risk`\n"
        f"━━━━━━━━━━━━━━━━━━\n"
    )

    return details

# Function to get domain information
async def get_domain_info(domain: str) -> str:
    url = f"https://api.domainsdb.info/v1/domains/search?domain={domain}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return f"Invalid domain name: {domain}"
            data = await response.json()

    if "domains" not in data or not data["domains"]:
        return f"Invalid domain name: {domain}"
    
    domain_info = data["domains"][0]
    domain_name = domain_info.get("domain", "Unknown")
    registrar = domain_info.get("registrar", "Unknown")
    registration = domain_info.get("create_date", "Unknown")
    expiration = domain_info.get("update_date", "Unknown")
    domain_available = "✅" if domain_info.get("isDead", False) else "❌"

    details = (
        f"**Domain:** `{domain_name}`\n"
        f"**Registrar:** `{registrar}`\n"
        f"**Registration:** `{registration}`\n"
        f"**Expiration:** `{expiration}`\n"
        f"**Domain Available:** {domain_available}\n"
    )

    return details

# Function to check proxy status by attempting to access Google
async def check_proxy(proxy: str, auth: tuple = None) -> str:
    url = "https://www.google.com"
    proxies = {
        "http": f"http://{proxy}",
        "https": f"https://{proxy}",
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=proxies, auth=aiohttp.BasicAuth(*auth) if auth else None, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    region = data.get("region", "Unknown")
                    return (
                        f"**Proxy:** `{proxy}`\n"
                        f"**Type:** `HTTP/HTTPS`\n"
                        f"**Status:** ☑️ `Alive`\n"
                        f"**Region:** `{region}`\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                    )
                else:
                    return (
                        f"**Proxy:** `{proxy}`\n"
                        f"**Type:** `HTTP/HTTPS`\n"
                        f"**Status:** 🔴 `Dead`\n"
                        f"**Region:** `Unknown`\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                    )
    except aiohttp.ClientError as e:
        return (
            f"**Proxy:** `{proxy}`\n"
            f"**Type:** `HTTP/HTTPS`\n"
            f"**Status:** 🔴 `Dead`\n"
            f"**Region:** `Unknown`\n"
            f"━━━━━━━━━━━━━━━━━━\n"
        )

# Function to extract text from an image using OCR
async def ocr_handler(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.reply_text("**❌ Please reply to an image with this command to extract text.**", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    fetching_msg = await message.reply_text("**⚡️Processing Your Request...⏳**", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    
    photo = await message.reply_to_message.download()
    img = Image.open(photo)
    text = pytesseract.image_to_string(img, lang='eng')

    if message.from_user:
        user_full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
        user_info = f"Text Extracted By: [{user_full_name}](tg://user?id={message.from_user.id})"
    else:
        group_name = message.chat.title or "this group"
        group_url = f"https://t.me/{message.chat.username}" if message.chat.username else "this group"
        user_info = f"Text Extracted By: [{group_name}]({group_url})"

    if not text.strip():
        response = f"**No readable text found in the image**\n\n{user_info}"
    else:
        text = f"```\n{text}\n```"  # Convert text to code format
        response = f"**Here's the Extracted Text:**\n━━━━━━━━━━━━━━━━\n{text}\n\n{user_info}"

    await fetching_msg.delete()
    await message.reply_text(response, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

# Function to extract YouTube video tags using yt-dlp
async def ytag_handler(client: Client, message: Message):
    if len(message.command) <= 1:
        await message.reply_text("**❌Please provide a YouTube URL. Usage: /ytag [URL]**", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    url = message.command[1]
    fetching_msg = await message.reply_text("**⚡️Processing Your Request...⏳**", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'force_generic_extractor': True,
        'cookiefile': YT_COOKIES_PATH,  # Correct path to your cookie file
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            tags = info_dict.get('tags', [])

        if not tags:
            response = "**Sorry, no tags available for this video.**"
        else:
            tags_str = "\n".join([f"`{tag}`" for tag in tags])
            response = f"**Your Requested Video Tags ✅**\n━━━━━━━━━━━━━━━━\n{tags_str}"

    except Exception as e:
        response = f"**An error occurred: {str(e)}**"

    await fetching_msg.delete()
    await message.reply_text(response, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

# Function to verify a Stripe key
async def verify_stripe_key(stripe_key: str) -> str:
    url = "https://api.stripe.com/v1/account"
    headers = {
        "Authorization": f"Bearer {stripe_key}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return "**The Stripe key is live.**"
            else:
                return "**The Stripe key is dead.**"

# Function to get information about a Stripe key
async def get_stripe_key_info(stripe_key: str) -> str:
    url = "https://api.stripe.com/v1/account"
    headers = {
        "Authorization": f"Bearer {stripe_key}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                return "**Unable to retrieve information for the provided Stripe key.**"
            data = await response.json()
    
    details = (
        f"**Stripe Key Information:**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"**ID:** `{data.get('id', 'N/A')}`\n"
        f"**Email:** `{data.get('email', 'N/A')}`\n"
        f"**Country:** `{data.get('country', 'N/A')}`\n"
        f"**Business Name:** `{data.get('business_name', 'N/A')}`\n"
        f"**Type:** `{data.get('type', 'N/A')}`\n"
        f"**Payouts Enabled:** `{data.get('payouts_enabled', 'N/A')}`\n"
        f"**Details Submitted:** `{data.get('details_submitted', 'N/A')}`\n"
        f"━━━━━━━━━━━━━━━━━━\n"
    )
    return details

# Handlers for the Pyrogram bot
async def ip_info_handler(client: Client, message: Message):
    if len(message.command) <= 1:
        await message.reply_text("**❌ Please provide a single IP address.**", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    ip = message.command[1]
    fetching_msg = await message.reply_text("**⚡️Fetching IP Info Please Wait.....⏳**", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    
    details = await get_ip_info(ip)

    if message.from_user:
        user_full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
        user_info = f"\n**Ip-Info Grab By:** [{user_full_name}](tg://user?id={message.from_user.id})"
    else:
        group_name = message.chat.title or "this group"
        group_url = f"https://t.me/{message.chat.username}" if message.chat.username else "this group"
        user_info = f"\n**Ip-Info Grab By:** [{group_name}]({group_url})"

    details += user_info

    await fetching_msg.delete()
    await message.reply_text(details, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

async def domain_info_handler(client: Client, message: Message):
    if len(message.command) <= 1:
        await message.reply_text("**❌ Please provide a valid domain name.**", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    fetching_msg = await message.reply_text("**⚡️Fetching Domain Information.....⏳**", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    
    domains = message.command[1:]
    details_list = []
    for domain in domains:
        details = await get_domain_info(domain)
        details_list.append(details)
    
    details_combined = "\n".join(details_list)

    if message.from_user:
        user_full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
        user_info = f"\n**Domain Info Grab By:** [{user_full_name}](tg://user?id={message.from_user.id})"
    else:
        group_name = message.chat.title or "this group"
        group_url = f"https://t.me/{message.chat.username}" if message.chat.username else "this group"
        user_info = f"\n**Domain Info Grab By:** [{group_name}]({group_url})"

    details_combined += user_info

    await fetching_msg.delete()
    await message.reply_text(details_combined, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

async def proxy_info_handler(client: Client, message: Message):
    if len(message.command) <= 1:
        await message.reply_text("**❌ Please provide at least one proxy.**", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    proxies = message.command[1:]
    auth = None

    if len(proxies) >= 3 and ':' not in proxies[-1]:
        user = proxies[-2]
        password = proxies[-1]
        auth = (user, password)
        proxies = proxies[:-2]

    fetching_msg = await message.reply_text("**⚡️Checking Proxies Please Wait.....⏳**", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

    details_list = []
    for proxy in proxies:
        details = await check_proxy(proxy, auth)
        details_list.append(details)
    
    details_combined = "\n".join(details_list)

    if message.from_user:
        user_full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
        user_info = f"\n**Proxies Checked By:** [{user_full_name}](tg://user?id={message.from_user.id})"
    else:
        group_name = message.chat.title or "this group"
        group_url = f"https://t.me/{message.chat.username}" if message.chat.username else "this group"
        user_info = f"\n**Proxies Checked By:** [{group_name}]({group_url})"

    details_combined += user_info

    await fetching_msg.delete()
    await message.reply_text(details_combined, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

async def stripe_key_handler(client: Client, message: Message):
    if len(message.command) <= 1:
        await message.reply_text("**❌Please provide a Stripe key. Usage: /sk [Stripe Key]**", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    stripe_key = message.command[1]
    fetching_msg = await message.reply_text("**⚡️Processing Your Request...⏳**", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    
    result = await verify_stripe_key(stripe_key)

    await fetching_msg.delete()
    await message.reply_text(result, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

async def stripe_key_info_handler(client: Client, message: Message):
    if len(message.command) <= 1:
        await message.reply_text("**❌Please provide a Stripe key. Usage: /skinfo [Stripe Key]**", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    stripe_key = message.command[1]
    fetching_msg = await message.reply_text("**⚡️Processing Your Request...⏳**", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    
    result = await get_stripe_key_info(stripe_key)

    await fetching_msg.delete()
    await message.reply_text(result, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

# Function to set up handlers for the Pyrogram bot
def setup_ip_handlers(app: Client):
    @app.on_message(filters.command(["ip", ".ip"], prefixes=["/", "."]) & (filters.private | filters.group))
    async def ip_info(client: Client, message: Message):
        await ip_info_handler(client, message)

    @app.on_message(filters.command(["dmn", ".dmn"], prefixes=["/", "."]) & (filters.private | filters.group))
    async def domain_info(client: Client, message: Message):
        await domain_info_handler(client, message)

    @app.on_message(filters.command(["px", ".px"], prefixes=["/", "."]) & (filters.private | filters.group))
    async def proxy_info(client: Client, message: Message):
        await proxy_info_handler(client, message)

    @app.on_message(filters.command(["ocr", ".ocr"], prefixes=["/", "."]) & (filters.private | filters.group))
    async def ocr_extract(client: Client, message: Message):
        await ocr_handler(client, message)

    @app.on_message(filters.command(["ytag", ".ytag"], prefixes=["/", "."]) & (filters.private | filters.group))
    async def ytag_info(client: Client, message: Message):
        await ytag_handler(client, message)

    @app.on_message(filters.command(["sk", ".sk"], prefixes=["/", "."]) & (filters.private | filters.group))
    async def stripe_key(client: Client, message: Message):
        await stripe_key_handler(client, message)

    @app.on_message(filters.command(["skinfo", ".skinfo"], prefixes=["/", "."]) & (filters.private | filters.group))
    async def stripe_key_info(client: Client, message: Message):
        await stripe_key_info_handler(client, message)
