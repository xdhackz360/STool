import os
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode, ChatType

API_BASE_URL = "https://webss.yasirapi.eu.org/api"

async def capture_screenshot(client: Client, message: Message):
    # Get the command and its arguments
    command_parts = message.text.split()
    
    # Check if a URL is provided
    if len(command_parts) < 2:
        await message.reply_text("**❌ Please Give At Least One URL**", parse_mode=ParseMode.MARKDOWN)
        return
    
    url = command_parts[1]
    
    # Add "https://www." to the URL if it's not present
    if not url.startswith("https://www."):
        url = "https://www." + url
    
    # Inform the user that the screenshot capturing process has started
    capturing_message = await message.reply_text("**⚡️ Capturing Screenshot Please Wait..⏳**", parse_mode=ParseMode.MARKDOWN)
    
    # Construct the API URL
    api_url = f"{API_BASE_URL}?url={url}&width=1280&height=720"
    
    try:
        # Capture the screenshot using the API
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                if resp.status == 200:
                    # Generate a file name using user or group information
                    if message.from_user:
                        file_name = f"screenshot_{message.from_user.id}.png"
                    else:
                        file_name = f"screenshot_{message.chat.id}.png"
                    
                    # Save the screenshot to a file
                    with open(file_name, 'wb') as f:
                        f.write(await resp.read())
                    
                    # Send the screenshot to the user
                    await client.send_photo(message.chat.id, file_name)
                    
                    # Delete the screenshot file
                    os.remove(file_name)
                else:
                    await message.reply_text("**❌ Sorry, Failed To Save Screenshot**", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await message.reply_text(f"**❌ Sorry, Failed To Save Screenshot**\n**Error:** {str(e)}", parse_mode=ParseMode.MARKDOWN)
    
    # Delete the "Capturing Screenshot" message
    await capturing_message.delete()

def setup_ss_handler(app: Client):
    @app.on_message(filters.command(["ss"], prefixes=["/", "."]) & (filters.private | filters.group))
    async def ss_command(client: Client, message: Message):
        await capture_screenshot(client, message)
