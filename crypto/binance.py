import requests
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

async def get_crypto_data(symbol):
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}USDT"
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, requests.get, url)
    if response.status_code != 200:
        raise ValueError(f"❌ Invalid token symbol or data unavailable for {symbol}")
    data = response.json()
    return data

def setup_binance_handler(app: Client):
    @app.on_message(filters.command(["price"], prefixes=["/", "."]) & (filters.private | filters.group))
    async def handle_price_command(client: Client, message: Message):
        if len(message.command) == 1 and not message.reply_to_message:
            await message.reply_text(
                "<b>❌ Specify a valid cryptocurrency name. e.g. /price BTC</b>",
                parse_mode=ParseMode.HTML
            )
        else:
            token = message.text.split(maxsplit=1)[1] if len(message.command) > 1 else message.reply_to_message.text.strip()
            fetching_message = await message.reply_text(
                "<b>Fetching token data, please wait...</b>",
                parse_mode=ParseMode.HTML
            )
            try:
                data = await get_crypto_data(token)
                result = (
                    f"<b>{token} (USDT)</b>\n"
                    f"    🔸 <b>Price:</b> <code>${data['lastPrice']} USDT</code>\n"
                    f"    🔸 <b>24hr Change:</b> <code>{data['priceChangePercent']}%</code>\n"
                    f"    🔸 <b>24hr High:</b> <code>${data['highPrice']} USDT</code>\n"
                    f"    🔸 <b>24hr Low:</b> <code>${data['lowPrice']} USDT</code>\n"
                )
                await fetching_message.delete()
                await message.reply_text(result, parse_mode=ParseMode.HTML)
            except ValueError as e:
                await fetching_message.delete()
                await message.reply_text(
                    f"<b>{str(e)}</b>",
                    parse_mode=ParseMode.HTML
                )
            except Exception as e:
                await fetching_message.delete()
                await message.reply_text(
                    f"<b>❌ An unexpected error occurred:</b> {str(e)}",
                    parse_mode=ParseMode.HTML
                )
