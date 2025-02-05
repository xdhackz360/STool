import requests
import aiohttp
from pyrogram import Client, filters
from pyrogram.enums import ParseMode

# Function to fetch GPT response from the API
async def fetch_gpt_response(prompt, model):
    url = f"https://darkness.ashlynn.workers.dev/chat/?prompt={prompt}&model={model}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_data = await response.json()
            return response_data.get('response', None)

def setup_gpt_handlers(app: Client):
    @app.on_message(filters.command(["gpt4"], prefixes=["/", "."]) & (filters.private | filters.group))
    async def gpt4_handler(client, message):
        await message.reply_text("**GPT-4 Gate Off 🔕**", parse_mode=ParseMode.MARKDOWN)

    @app.on_message(filters.command(["gpt"], prefixes=["/", "."]) & (filters.private | filters.group))
    async def gpt_handler(client, message):
        try:
            # Check if a prompt is provided
            if len(message.command) <= 1:
                await message.reply_text("**❌Please provide a prompt for GPT response**", parse_mode=ParseMode.MARKDOWN)
                return

            prompt = " ".join(message.command[1:])
            # Send a temporary message indicating the bot is generating a response
            loading_message = await message.reply_text("**⚡️Generating GPT Response Please Wait....⌛️**", parse_mode=ParseMode.MARKDOWN)
            # Fetch response from the API
            response_text = await fetch_gpt_response(prompt, "gpt-4o-mini")
            
            # Delete the loading message
            await loading_message.delete()
            
            if response_text:
                # Send the response text to the user
                await message.reply_text(response_text, parse_mode=ParseMode.MARKDOWN)
            else:
                await message.reply_text("**Error Generating Response...**", parse_mode=ParseMode.MARKDOWN)
        except Exception:
            await message.reply_text("**Error Generating Response...**", parse_mode=ParseMode.MARKDOWN)
