import requests
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import NEWS_API_KEY
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Fetch news from the API
def fetch_news(country_code, next_page=None):
    url = f"https://newsdata.io/api/1/news?country={country_code}&apikey={NEWS_API_KEY}"
    if next_page:
        url += f"&page={next_page}"
    response = requests.get(url)
    response_json = response.json()
    logging.info(f"Fetched news: {response_json}")
    if response_json.get("status") == "error":
        raise ValueError(response_json["results"]["message"])
    return response_json

# Send news in a formatted message with pagination
def send_news(client, chat_id, data, country_code, next_page_token=None, prev_page_token=None):
    news_list = data.get("results", [])
    if not news_list:
        client.send_message(chat_id, "No news found.")
        return

    text = "*Top Headlines*\n"
    for news in news_list:
        title = news.get('title', 'No title')
        source_name = news.get('source_name', 'Unknown source')
        pub_date = news.get('pubDate', 'Unknown date')
        link = news.get('link', '#')
        text += f"━━━━━━━━━━━━━━━━\n"
        text += f"📰 *Title:* {title}\n"
        text += f"🏢 *Source:* {source_name}\n"
        text += f"⏰ *Publish At:* {pub_date}\n"
        text += f"🔗 [Read More]({link})\n\n"

    buttons = []
    if prev_page_token:
        buttons.append(InlineKeyboardButton("Previous", callback_data=f"{country_code}_prev_{prev_page_token}"))
    if next_page_token:
        buttons.append(InlineKeyboardButton("Next", callback_data=f"{country_code}_next_{next_page_token}"))

    reply_markup = InlineKeyboardMarkup([buttons])
    client.send_message(chat_id, text, reply_markup=reply_markup, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)

# Setup news handlers
def setup_news_handler(app):
    @app.on_message(filters.command(["news"], prefixes=["/", "."]) & (filters.private | filters.group))
    def news(client, message):
        try:
            country_code = message.command[1].upper()
            logging.info(f"Received country code: {country_code}")
            data = fetch_news(country_code)
            next_page_token = data.get("nextPage")
            send_news(client, message.chat.id, data, country_code, next_page_token)
        except IndexError:
            message.reply("Please provide a valid country code (e.g., /news bd).")
        except ValueError as e:
            logging.error(f"Error fetching news: {e}")
            message.reply(str(e))
        except Exception as e:
            logging.error(f"Error handling news command: {e}")
            message.reply("An error occurred while fetching the news.")

    @app.on_callback_query(filters.regex(r"(\w+)_prev_(.+)"))
    def prev_page(client, callback_query):
        try:
            country_code, prev_page_token = callback_query.data.split("_")[0], callback_query.data.split("_")[2]
            logging.info(f"Handling previous page: {country_code}, {prev_page_token}")
            data = fetch_news(country_code, prev_page_token)
            next_page_token = data.get("nextPage")
            send_news(client, callback_query.message.chat.id, data, country_code, next_page_token, prev_page_token)
            callback_query.message.delete()
        except ValueError as e:
            logging.error(f"Error fetching news: {e}")
            callback_query.message.reply(str(e))
        except Exception as e:
            logging.error(f"Error handling previous page: {e}")
            callback_query.message.reply("An error occurred while fetching the news.")

    @app.on_callback_query(filters.regex(r"(\w+)_next_(.+)"))
    def next_page(client, callback_query):
        try:
            country_code, next_page_token = callback_query.data.split("_")[0], callback_query.data.split("_")[2]
            logging.info(f"Handling next page: {country_code}, {next_page_token}")
            data = fetch_news(country_code, next_page_token)
            prev_page_token = callback_query.data.split("_")[2]  # Use the current token as the previous token for the next fetch
            send_news(client, callback_query.message.chat.id, data, country_code, data.get("nextPage"), prev_page_token)
            callback_query.message.delete()
        except ValueError as e:
            logging.error(f"Error fetching news: {e}")
            callback_query.message.reply(str(e))
        except Exception as e:
            logging.error(f"Error handling next page: {e}")
            callback_query.message.reply("An error occurred while fetching the news.")
