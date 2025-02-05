from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from datetime import datetime, timedelta
import pymongo
from config import MONGO_URL, OWNERS

client = pymongo.MongoClient(MONGO_URL)
db = client["user_activity_db"]
user_activity_collection = db["user_activity"]

# Global dictionary to hold user-specific data
user_data = {}

# Function to update user activity in the MongoDB database
def update_user_activity(user_id):
    now = datetime.utcnow()
    user = user_activity_collection.find_one({"user_id": user_id})
    if not user:
        user_activity_collection.insert_one({
            "user_id": user_id,
            "last_activity": now,
            "daily": 0,
            "weekly": 0,
            "monthly": 0,
            "yearly": 0
        })
    else:
        user_activity_collection.update_one(
            {"user_id": user_id},
            {"$set": {"last_activity": now}},
            upsert=True
        )
        user_activity_collection.update_one(
            {"user_id": user_id},
            {"$inc": {"daily": 1, "weekly": 1, "monthly": 1, "yearly": 1}},
        )

# Function to handle the /send command (works in private)
async def send_handler(client: Client, message: Message):
    if message.from_user.id not in OWNERS:
        return

    if len(message.command) == 1:
        await message.reply_text("**Please Enter The Message To Broadcast 😎**", parse_mode=ParseMode.MARKDOWN)
        return

    broadcast_message = message.text.split(None, 1)[1]

    # Ask if the owner wants to add buttons
    buttons_choice = InlineKeyboardMarkup([
        [InlineKeyboardButton("Yes", callback_data="add_buttons_yes"),
         InlineKeyboardButton("No", callback_data="add_buttons_no")]
    ])
    await message.reply_text("**Do You Want To Add Buttons?**", reply_markup=buttons_choice, parse_mode=ParseMode.MARKDOWN)

    # Save the message ID and text for further use
    user_data[message.from_user.id] = {
        "message_id": message.id,  # Corrected attribute
        "text": f"**{broadcast_message}**",  # Make the message bold
        "reply_to_message_id": message.reply_to_message.id if message.reply_to_message else None,
        "chat_id": message.chat.id  # Store the chat id to use in copy_message
    }

# Function to handle callback queries for adding buttons
async def callback_query_handler(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id
    user_info = user_data.get(user_id, {})

    if data == "add_buttons_yes":
        # Send tutorial for adding buttons
        tutorial_message = (
            "**Please send the buttons in the following format:**\n"
            "`(Button Name 1): URL 1`\n"
            "`(Button Name 2): URL 2`\n"
            "**Example:**\n"
            "`(Update Channel): https://t.me/ModVipRM`\n"
            "`(Developer): https://t.me/abirxdhackz`"
        )
        await callback_query.message.edit_text(tutorial_message, parse_mode=ParseMode.MARKDOWN)
        user_info["awaiting_buttons"] = True
        user_data[user_id] = user_info

    elif data == "add_buttons_no":
        # Broadcast the message without buttons
        await broadcast_message(client, user_info["text"], user_info["reply_to_message_id"], user_info["chat_id"])
        await callback_query.message.edit_text("**Broadcast Successfully Sent to all users**", parse_mode=ParseMode.MARKDOWN)
        user_data.pop(user_id, None)

    elif data == "proceed_broadcast_yes":
        # Proceed with broadcasting the message with buttons
        await broadcast_message(client, user_info["text"], user_info["reply_to_message_id"], user_info["chat_id"], user_info.get("buttons"))
        await callback_query.message.edit_text("**Broadcast Successfully Sent to all users**", parse_mode=ParseMode.MARKDOWN)
        user_data.pop(user_id, None)

    elif data == "proceed_broadcast_no":
        # Cancel the broadcast process
        await callback_query.message.edit_text("**Broadcast Cancelled**", parse_mode=ParseMode.MARKDOWN)
        user_data.pop(user_id, None)

# Function to handle messages with button data
async def button_data_handler(client: Client, message: Message):
    user_id = message.from_user.id
    user_info = user_data.get(user_id, {})

    if message.from_user.id not in OWNERS or not user_info.get("awaiting_buttons"):
        return

    button_lines = message.text.split('\n')
    buttons = []

    for line in button_lines:
        if line.startswith('(') and ')' in line and ':' in line:
            try:
                button_name = line[line.find('(') + 1:line.find(')')].strip()
                button_url = line[line.find(':') + 1:].strip()
                buttons.append(InlineKeyboardButton(button_name, url=button_url))
            except Exception as e:
                print(f"Failed to parse button: {line}. Error: {e}")

    user_info["buttons"] = buttons
    user_info["awaiting_buttons"] = False
    user_data[user_id] = user_info

    # Confirm with the owner if they want to proceed with broadcasting
    proceed_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Yes", callback_data="proceed_broadcast_yes"),
         InlineKeyboardButton("No", callback_data="proceed_broadcast_no")]
    ])
    await message.reply_text("**Should I Proceed NOW?**", reply_markup=proceed_buttons, parse_mode=ParseMode.MARKDOWN)

# Function to broadcast message to all users
async def broadcast_message(client: Client, text, reply_to_message_id=None, from_chat_id=None, buttons=None):
    sent_count = 0
    keyboard = InlineKeyboardMarkup(
        [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    ) if buttons else None

    for user in user_activity_collection.find():
        try:
            if reply_to_message_id:
                await client.copy_message(
                    chat_id=user["user_id"],
                    from_chat_id=from_chat_id,  # Use stored chat_id
                    message_id=reply_to_message_id,
                    reply_markup=keyboard
                )
            else:
                await client.send_message(
                    chat_id=user["user_id"],
                    text=text,  # Message is already bold
                    reply_markup=keyboard,
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True
                )
            sent_count += 1
        except Exception as e:
            print(f"Failed to send message to {user['user_id']}: {e}")

# Function to handle the /stats command (works in both private and group)
async def stats_handler(client: Client, message: Message):
    now = datetime.utcnow()
    daily_users = user_activity_collection.count_documents({"last_activity": {"$gt": now - timedelta(days=1)}})
    weekly_users = user_activity_collection.count_documents({"last_activity": {"$gt": now - timedelta(weeks=1)}})
    monthly_users = user_activity_collection.count_documents({"last_activity": {"$gt": now - timedelta(days=30)}})
    yearly_users = user_activity_collection.count_documents({"last_activity": {"$gt": now - timedelta(days=365)}})
    total_users = user_activity_collection.count_documents({})

    stats_text = (
        "**Smart Bot Status ⇾ Report ✅**\n"
        "**━━━━━━━━━━━━━━━━**\n"
        "**Name:** Smart Tool ⚙️\n"
        "**Version:** 3.0 (Beta Testing) 🛠\n\n"
        "**Development Team:**\n"
        "**- Creator:** [⏤͞〲ᗩᗷiᖇ 𓊈乂ᗪ𓊉 👨‍💻](https://t.me/abirxdhackz)\n"
        "**Technical Stack:**\n"
        "**- Language:** Python 🐍\n"
        "**- Libraries:** Aiogram, Pyrogram, and Telethon 📚\n"
        "**- Database:** MongoDB Database 🗄\n"
        "**- Hosting:** Hostinger VPS 🌐\n\n"
        "**About:** Smart Tool ⚙️ The ultimate Telegram toolkit! Education, AI, downloaders, temp mail, finance tools & more—simplify life!\n\n"
        ">🔔 For Bot Update News: [Join Now](https://t.me/ModVipRM)\n"
        "**━━━━━━━━━━━━━━━━**\n"
        f"**1 Day:** {daily_users} users were active\n"
        f"**1 Week:** {weekly_users} users were active\n"
        f"**1 Month:** {monthly_users} users were active\n"
        f"**1 Year:** {yearly_users} users were active\n"
        "**━━━━━━━━━━━━━━━━**\n"
        f"**Total Smart Tools Users:** {total_users}"
    )

    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔔 Bot Updates", url="https://t.me/ModVipRM")]])
    await message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard, disable_web_page_preview=True)

# Function to set up the admin handlers for the bot
def setup_admin_handlers(app: Client):
    """
    Set up command handlers for the Pyrogram bot.
    This includes specific commands like /send and /stats, as well as general activity tracking.
    """
    # Add the /send command handler for broadcasting messages
    app.add_handler(
        MessageHandler(send_handler, filters.command("send") & filters.private),
        group=1,  # High priority to ensure it executes first
    )
    
    # Add the /stats command handler for bot statistics (works in both private and group)
    app.add_handler(
        MessageHandler(stats_handler, filters.command("stats")),
        group=1,  # High priority to ensure it executes first
    )
    
    # Add a general handler to track all user activity
    app.add_handler(
        MessageHandler(lambda client, message: update_user_activity(message.from_user.id) if message.from_user else None, filters.all),
        group=2,  # Lower priority so it runs after command handlers
    )

    # Add the callback query handler
    app.add_handler(
        CallbackQueryHandler(callback_query_handler),
        group=1  # High priority to ensure it executes first
    )

    # Add the button data handler
    app.add_handler(
        MessageHandler(button_data_handler, filters.text & filters.private),
        group=1  # High priority to ensure it executes first
    )
