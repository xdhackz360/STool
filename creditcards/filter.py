import re
import os
import asyncio
import requests
from collections import Counter
from pyrogram import Client, filters, handlers
from pyrogram.enums import ParseMode
from pyrogram.types import Message

# Function to fetch BIN information
async def fetch_bin_info(bin_number):
    """Fetch BIN information from the API."""
    url = f"https://data.handyapi.com/bin/{bin_number}"
    headers = {'Referer': 'your-domain'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

# Function to filter valid CC details from a file
async def filter_valid_cc(content):
    """Filter valid credit card details from the file content."""
    valid_cc_pattern = re.compile(r'^\d{16}\|\d{2}\|\d{4}\|\d{3}$')
    valid_ccs = [line.strip() for line in content if valid_cc_pattern.match(line.strip())]
    return valid_ccs

# Command to filter credit card details from a file
async def handle_fcc_command(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.document or not message.reply_to_message.document.file_name.endswith('.txt'):
        await message.reply_text("<b>⚠️ Reply to a text file to filter CC details❌</b>", parse_mode=ParseMode.HTML)
        return

    temp_msg = await message.reply_text("<b>⚡️ Filtering CCs, Please Wait...⏳ </b>", parse_mode=ParseMode.HTML)
    file_path = await message.reply_to_message.download()
    with open(file_path, 'r') as file:
        content = file.readlines()

    valid_ccs = await filter_valid_cc(content)
    if not valid_ccs:
        await temp_msg.delete()
        await message.reply_text("<b>❌ No valid credit card details found in the file.</b>", parse_mode=ParseMode.HTML)
        os.remove(file_path)
        return

    if message.from_user:
        user_full_name = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()
        user_profile_url = f"https://t.me/{message.from_user.username}" if message.from_user.username else None
        user_link = f'<a href="{user_profile_url}">{user_full_name}</a>' if user_profile_url else user_full_name
    else:
        group_name = message.chat.title or "this group"
        group_url = f"https://t.me/{message.chat.username}" if message.chat.username else "this group"
        user_link = f'<a href="{group_url}">{group_name}</a>'

    if len(valid_ccs) > 10:
        file_name = "Smart_Tool_⚙️_CC_Results.txt"
        with open(file_name, 'w') as f:
            f.write("\n".join(valid_ccs))
        caption = (
            f"<b>Here are the filtered cards:</b>\n"
            f"<b>━━━━━━━━━━━━━━</b>\n"
            f"<b>Total cards found:</b> <code>{len(valid_ccs)}</code>\n"
            f"<b>━━━━━━━━━━━━━━</b>\n"
            f"<b>Filter By:</b> {user_link}\n"
        )
        await temp_msg.delete()
        await client.send_document(message.chat.id, file_name, caption=caption, parse_mode=ParseMode.HTML)
        os.remove(file_name)
    else:
        formatted_ccs = "\n".join(valid_ccs)
        response_message = (
            f"<b>Total cards found: {len(valid_ccs)}</b>\n\n"
            f"<code>{formatted_ccs}</code>\n\n"
            f"<b>Filtered By:</b> {user_link}"
        )
        await temp_msg.delete()
        await message.reply_text(response_message, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    
    os.remove(file_path)

# Command to display top bins from a file
async def handle_topbin_command(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.document or not message.reply_to_message.document.file_name.endswith('.txt'):
        await message.reply_text("<b>⚠️ Reply to a text file containing credit cards to check top bins❌</b>", parse_mode=ParseMode.HTML)
        return

    temp_msg = await message.reply_text("<b>Finding Top Bins...</b>", parse_mode=ParseMode.HTML)
    file_path = await message.reply_to_message.download()
    with open(file_path, 'r') as file:
        content = file.readlines()

    bin_counter = Counter([line.strip()[:6] for line in content])
    top_bins = bin_counter.most_common(20)

    if not top_bins:
        await temp_msg.delete()
        await message.reply_text("<b>❌ No BIN data found in the file.</b>", parse_mode=ParseMode.HTML)
        os.remove(file_path)
        return

    if message.from_user:
        user_full_name = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()
        user_profile_url = f"https://t.me/{message.from_user.username}" if message.from_user.username else None
        user_link = f'<a href="{user_profile_url}">{user_full_name}</a>' if user_profile_url else user_full_name
    else:
        group_name = message.chat.title or "this group"
        group_url = f"https://t.me/{message.chat.username}" if message.chat.username else "this group"
        user_link = f'<a href="{group_url}">{group_name}</a>'

    response_message = (
        f"<b>Here are the top 20 bins:</b>\n"
        f"━━━━━━━━━━━━━━━━\n"
    )
    for i, (bin, count) in enumerate(top_bins, 1):
        response_message += f"{i:02d}. BIN: `{bin}` - Count: `{count}`\n"

    response_message += f"\n<b>Checked By:</b> {user_link}"

    await temp_msg.delete()
    await message.reply_text(response_message, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    os.remove(file_path)

# Setup handlers
def setup_filter_handlers(app: Client):
    app.add_handler(handlers.MessageHandler(handle_fcc_command, filters.command(["fcc", "topbin"], prefixes=["/", "."]) & (filters.private | filters.group)))
