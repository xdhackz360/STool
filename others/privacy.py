from pyrogram import Client, filters
from pyrogram.enums import ParseMode, ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Define your privacy policy text
PRIVACY_POLICY = """
<b>Privacy Policy for Smart Tool ⚙️</b>
━━━━━━━━━━━━━━━━━

Welcome to Smart Tool ⚙️, the ultimate toolkit on Telegram, offering a variety of features to simplify your tasks. By using Smart Tool ⚙️, you agree to the terms and conditions of this policy.

<b>Information We Collect</b>

1. <b>Personal Information:</b>
   - User ID and Username: We collect your User ID and username to provide personalized services.

2. <b>Usage Data:</b>
   - We collect data on commands used, tools accessed, and frequency of use to improve services.

<b>How We Use Your Information</b>

   - <b>Service Provision:</b> To provide and enhance the services offered by Smart Nexus.
   - <b>Communication:</b> To communicate with you about updates & new features.
   - <b>Security:</b> To monitor and protect against unauthorized access, and spammer.
   - <b>Promotions and Advertisements:</b> We may share paid promotions and advertisements through the bot.

<b>Data Security</b>

   - We use security measures to protect your information. 100% Secure All Info.

Thank you for using Smart Tool ⚙️. We are committed to protecting your privacy and ensuring an enjoyable experience with our bot.
"""

def setup_privacy_handler(app: Client):
    @app.on_message(filters.command(["privacy"], prefixes=["/", "."]) & (filters.private | filters.group))
    async def show_privacy_policy(client, message):
        await message.reply_text(
            PRIVACY_POLICY,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Close", callback_data="close_privacy_policy")]
            ])
        )

    @app.on_callback_query(filters.regex("close_privacy_policy"))
    async def close_privacy_policy(client, callback_query):
        await callback_query.message.delete()
