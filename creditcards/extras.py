import re
import os
from pyrogram import Client, filters, handlers
from pyrogram.enums import ParseMode
from pyrogram.types import Message

def filter_bin(content, bin_number):
    """Filter lines containing the specified BIN."""
    filtered_lines = [line for line in content if line.startswith(bin_number)]
    return filtered_lines

def remove_bin(content, bin_number):
    """Remove lines containing the specified BIN."""
    filtered_lines = [line for line in content if not line.startswith(bin_number)]
    return filtered_lines

async def process_file(file_path, bin_number, command):
    """Process the file to either filter or remove lines based on the command."""
    with open(file_path, 'r') as file:
        content = file.readlines()

    if command in ['/adbin', '.adbin']:
        return filter_bin(content, bin_number)
    elif command in ['/rmbin', '.rmbin']:
        return remove_bin(content, bin_number)

async def handle_bin_commands(client, message: Message):
    args = message.text.split()
    if len(args) != 2:
        await message.reply_text("<b>⚠️ Please provide a valid BIN number❌</b>", parse_mode=ParseMode.HTML)
        return

    command = args[0]
    bin_number = args[1]
    if not re.match(r'^\d{6}$', bin_number):
        await message.reply_text("<b>⚠️ BIN number must be 6 digits❌</b>", parse_mode=ParseMode.HTML)
        return

    if not message.reply_to_message:
        await message.reply_text("<b>⚠️ Please reply to a valid .txt file❌</b>", parse_mode=ParseMode.HTML)
        return

    if not message.reply_to_message.document or not message.reply_to_message.document.file_name.endswith('.txt'):
        await message.reply_text("<b>⚠️ Please reply to a valid .txt file❌</b>", parse_mode=ParseMode.HTML)
        return

    file_path = await message.reply_to_message.download()
    processed_cards = await process_file(file_path, bin_number, command)
    
    if not processed_cards:
        await message.reply_text(f"<b>❌ No credit card details found with BIN {bin_number}.</b>", parse_mode=ParseMode.HTML)
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

    if len(processed_cards) > 10:
        file_name = f"Smart Tool ⚙️ {command[1:]}.txt"
        with open(file_name, "w") as file:
            file.write("\n".join(processed_cards))

        caption = (
            f"Here are the {'filtered' if command in ['/adbin', '.adbin'] else 'remaining'} cards:\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"Total cc: {len(processed_cards)}\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"Filter By: {user_link}"
        )

        await message.reply_document(document=file_name, caption=caption, parse_mode=ParseMode.HTML)
        os.remove(file_name)
    else:
        formatted_cards = "\n".join(line.strip() for line in processed_cards)
        response_message = (
            f"<b>Here are the {'filtered' if command in ['/adbin', '.adbin'] else 'remaining'} cards:</b>\n\n"
            f"```\n{formatted_cards}\n```\n\n"
            f"<b>Total Cards:</b> <code>{len(processed_cards)}</code>\n"
            f"<b>Filter By:</b> {user_link}"
        )

        await message.reply_text(response_message, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    os.remove(file_path)

def setup_bin_handlers(app: Client):
    app.add_handler(handlers.MessageHandler(handle_bin_commands, filters.command(["adbin", "rmbin"], prefixes=["/", "."]) & (filters.private | filters.group)))
