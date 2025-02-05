import re
import os
import random
import requests
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
from config import BIN_KEY

def get_bin_info(bin):
    headers = {'x-api-key': 'BIN_KEY'}
    response = requests.get(f"https://data.handyapi.com/bin/{bin}", headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def luhn_algorithm(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10

def generate_credit_card(bin, amount, month=None, year=None):
    cards = []
    for _ in range(amount):
        while True:
            card_body = bin + ''.join([str(random.randint(0, 9)) for _ in range(15 - len(bin))])
            for check_digit in range(10):
                card_number = card_body + str(check_digit)
                if luhn_algorithm(card_number) == 0:
                    break
            card_month = month or f"{random.randint(1, 12):02}"
            card_year = year or random.randint(2024, 2029)
            cvv = ''.join([str(random.randint(0, 9)) for _ in range(3)])
            cards.append(f"{card_number}|{card_month}|{card_year}|{cvv}")
            break
    return cards

def parse_input(user_input):
    bin = None
    month = None
    year = None
    amount = 10

    match = re.match(r"(\d{6,12})(x{4})?\|?(\d{2})?\|?(\d{2,4})?\s*(\d+)?", user_input)
    if match:
        bin, suffix, month, year, amount = match.groups()
        if suffix:
            bin += suffix
        year = f"20{year}" if year and len(year) == 2 else year
        amount = int(amount) if amount else 10
        
    return bin, month, year, amount

def generate_custom_cards(bin, amount, month, year):
    cards = []
    for _ in range(amount):
        while True:
            card_body = ''.join([str(random.randint(0, 9)) if c in 'xX' else c for c in bin])
            for check_digit in range(10):
                card_number = card_body + str(check_digit)
                if luhn_algorithm(card_number) == 0:
                    break
            card_month = month or f"{random.randint(1, 12):02}"
            card_year = year or random.randint(2024, 2029)
            cvv = ''.join([str(random.randint(0, 9)) for _ in range(3)])
            cards.append(f"{card_number}|{card_month}|{card_year}|{cvv}")
            break
    return cards

def setup_credit_handlers(app: Client):
    @app.on_message(filters.command(["gen"], prefixes=["/", "."]) & (filters.private | filters.group))
    async def generate_handler(client: Client, message: Message):
        user_input = message.text.split(maxsplit=1)
        if len(user_input) == 1:
            await message.reply_text("**Provide a valid BIN at least 6 digits ❌**")
            return
        
        user_input = user_input[1]
        bin, month, year, amount = parse_input(user_input)

        if not bin or len(bin) < 6:
            await message.reply_text("**Provide a valid BIN at least 6 digits ❌**")
            return

        # Fetch BIN info
        bin_info = get_bin_info(bin[:6])
        if not bin_info or bin_info.get("Status") != "SUCCESS":
            await message.reply_text("**Invalid BIN provided ❌**")
            return

        bank = bin_info.get("Issuer")
        country_name = bin_info["Country"].get("Name", "Unknown")
        card_type = bin_info.get("Type", "Unknown")
        card_scheme = bin_info.get("Scheme", "Unknown")
        bank_text = bank.upper() if bank else "Unknown"
        bin_info_text = f"**Bank:** `{bank_text}`\n**Country:** `{country_name}`\n**BIN Info:** `{card_scheme.upper()} - {card_type.upper()}`"

        # Notify user that the bot is generating cards
        progress_message = await message.reply_text("**Generating Credit Cards...☑️**")

        # Generate credit cards
        if 'x' in bin.lower():
            cards = generate_custom_cards(bin, amount, month, year)
        else:
            cards = generate_credit_card(bin, amount, month, year)

        if amount <= 10:
            card_text = "\n".join([f"`{card}`" for card in cards])
            await progress_message.delete()
            response_text = f"**BIN ⇾ {bin}**\n**Amount ⇾ {amount}**\n\n{card_text}\n\n{bin_info_text}"
            callback_data = f"regenerate|{user_input}|{amount}"

            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton("Regenerate", callback_data=callback_data)]]
            )
            await message.reply_text(response_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        else:
            # Save cards to a file if amount is greater than 10
            file_name = f"{bin} x {amount}.txt"
            try:
                with open(file_name, "w") as file:
                    file.write("\n".join(cards))

                await progress_message.delete()
                if message.from_user:
                    user_full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
                    user_link = f"[{user_full_name}](tg://user?id={message.from_user.id})"
                else:
                    group_name = message.chat.title or "this group"
                    group_url = f"https://t.me/{message.chat.username}" if message.chat.username else "this group"
                    user_link = f"[{group_name}]({group_url})"

                caption = f"{amount} {card_scheme.upper()} {card_type.upper()} credit card numbers for BIN {bin}\n━━━━━━━━━━━━━━━━━━\n{bin_info_text}\n━━━━━━━━━━━━━━━━━━\nGenerated By: {user_link}"

                await message.reply_document(document=file_name, caption=caption, parse_mode=ParseMode.MARKDOWN)
            except Exception as e:
                await message.reply_text(f"**Failed to save or send document: {str(e)}**")
            finally:
                if os.path.exists(file_name):
                    os.remove(file_name)

    @app.on_callback_query(filters.regex(r"regenerate\|(.+?)\|(\d+)"))
    async def regenerate_callback(client: Client, callback_query):
        original_input, amount = callback_query.data.split('|')[1:]
        amount = int(amount)
        bin, month, year, _ = parse_input(original_input)

        # Fetch BIN info again
        bin_info = get_bin_info(bin[:6])
        if not bin_info or bin_info.get("Status") != "SUCCESS":
            await callback_query.answer("BIN info retrieval failed!", show_alert=True)
            return

        bank = bin_info.get("Issuer")
        country_name = bin_info["Country"].get("Name", "Unknown")
        card_type = bin_info.get("Type", "Unknown")
        card_scheme = bin_info.get("Scheme", "Unknown")
        bank_text = bank.upper() if bank else "Unknown"

        # Generate new credit cards
        if 'x' in bin.lower():
            cards = generate_custom_cards(bin, amount, month, year)
        else:
            cards = generate_credit_card(bin, amount, month, year)
        
        card_text = "\n".join([f"`{card}`" for card in cards[:10]])

        bin_info_text = f"**Bank:** `{bank_text}`\n**Country:** `{country_name}`\n**BIN Info:** `{card_scheme.upper()} - {card_type.upper()}`"
        response_text = f"**BIN ⇾ {bin}**\n**Amount ⇾ {amount}**\n\n{card_text}\n\n{bin_info_text}"

        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Regenerate", callback_data=f"regenerate|{original_input}|{amount}")]]
        )

        await callback_query.message.edit_text(response_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        await callback_query.answer("Generated new cards successfully!")

    @app.on_message(filters.command(["bin"], prefixes=["/", "."]) & (filters.private | filters.group))
    async def bin_handler(client: Client, message: Message):
        user_input = message.text.split(maxsplit=1)
        if len(user_input) == 1:
            await message.reply_text("**Provide a valid BIN (6 digits) ❌**")
            return

        bin = user_input[1]  # Take the full BIN

        # Fetch BIN info
        progress_message = await message.reply_text("**Fetching Bin Details...**")
        bin_info = get_bin_info(bin[:6])
        await progress_message.delete()

        if not bin_info or bin_info.get("Status") != "SUCCESS":
            await message.reply_text("**Invalid BIN provided ❌**")
            return

        bank = bin_info.get("Issuer", "Unknown")
        country_name = bin_info["Country"].get("Name", "Unknown")
        card_type = bin_info.get("Type", "Unknown")
        card_scheme = bin_info.get("Scheme", "Unknown")
        country_emoji = bin_info["Country"].get("Emoji", "")
        bank_text = bank.upper() if bank else "Unknown"

        bin_info_text = (
            f"**🔍 BIN Details 📋**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"• **BIN:** `{bin}`\n"
            f"• **INFO:** {card_scheme.upper()} - {card_type.upper()}\n"
            f"• **BANK:** {bank_text}\n"
            f"• **COUNTRY:** {country_name.upper()} {country_emoji}\n"
            f"━━━━━━━━━━━━━━━━━━"
        )

        await message.reply_text(bin_info_text, parse_mode=ParseMode.MARKDOWN)

    @app.on_message(filters.command(["mgn"], prefixes=["/", "."]) & (filters.private | filters.group))
    async def multigen_handler(client: Client, message: Message):
        user_input = message.text.split()
        if len(user_input) < 3:
            await message.reply_text("**Wrong args ❌**\nUse `/mgn [bin1] [bin2] ... [amount]`", parse_mode=ParseMode.MARKDOWN)
            return

        bins = user_input[1:-1]
        amount = int(user_input[-1])

        if any(len(bin) < 6 or len(bin) > 16 for bin in bins):
            await message.reply_text("**Each BIN should be between 6 and 16 digits ❌**")
            return

        total_cards = []
        for bin in bins:
            total_cards.extend(generate_credit_card(bin, amount))

        file_name = "Smart Tool ⚙️ Multigen.txt"
        try:
            with open(file_name, "w") as file:
                file.write("\n".join(total_cards))

            if message.from_user:
                user_full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
                user_link = f"[{user_full_name}](tg://user?id={message.from_user.id})"
            else:
                group_name = message.chat.title or "this group"
                group_url = f"https://t.me/{message.chat.username}" if message.chat.username else "this group"
                user_link = f"[{group_name}]({group_url})"

            caption = (
                f"**🔥 Generated {len(total_cards)} credit card numbers from all BIN 🔥**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🏦 **BINS:**\n" + "\n".join([f"• `{bin}`" for bin in bins]) + '\n'
                f"━━━━━━━━━━━━━━━━━━\n"
                f"Generated By: {user_link}"
            )

            await message.reply_document(document=file_name, caption=caption, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            await message.reply_text(f"**Failed to save or send document: {str(e)}**")
        finally:
            if os.path.exists(file_name):
                os.remove(file_name)
