import pytz
import pycountry
from datetime import datetime
import calendar
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Fixed holidays in Bangla with emojis
HOLIDAYS = {
    (2, 15): "শবে বরাত 🌙",
    (2, 21): "শহীদ দিবস 🕊️",
    (3, 26): "স্বাধীনতা দিবস 🇧🇩",
    (3, 27): "লাইলাতুল কদর 🌌",
    (3, 28): "জুমাতুল বিদা 🕌",
    (3, 29): "ঈদুল ফিতর ছুটি 🎉",
    (3, 30): "ঈদুল ফিতর ছুটি 🎉",
    (3, 31): "ঈদুল ফিতর 🕌",
    (4, 1): "ঈদুল ফিতর ছুটি 🎉",
    (4, 2): "ঈদুল ফিতর ছুটি 🎉",
    (4, 14): "বাংলা নববর্ষ 🎊",
    (5, 1): "মে দিবস ✊",
    (5, 11): "বুদ্ধ পূর্ণিমা 🕉️",
    (6, 5): "ঈদুল আজহা ছুটি 🐄",
    (6, 6): "ঈদুল আজহা ছুটি 🐄",
    (6, 7): "ঈদুল আজহা 🕌",
    (6, 8): "ঈদুল আজহা ছুটি 🐄",
    (6, 9): "ঈদুল আজহা ছুটি 🐄",
    (6, 10): "ঈদুল আজহা ছুটি 🐄",
    (7, 6): "আশুরা 🌙",
    (8, 15): "জাতীয় শোক দিবস 🖤",
    (8, 16): "শুভ জন্মাষ্টমী 🙏",
    (9, 5): "ঈদে মিলাদুন্নবী ﷺ",
    (10, 2): "বিজয়া দশমী 🪔",
    (12, 16): "বিজয় দিবস 🇧🇩",
    (12, 25): "বড়দিন 🎄",
}

async def get_calendar_markup(year, month, country_code):
    # Create a calendar object
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month)
    now = datetime.now()

    # Navigation buttons
    prev_month = month - 1 if month > 1 else 12
    next_month = month + 1 if month < 12 else 1
    prev_year = year - 1 if month == 1 else year
    next_year = year + 1 if month == 12 else year

    navigation_buttons = [
        InlineKeyboardButton("<", callback_data=f"calendar_{country_code}_{prev_year}_{prev_month}"),
        InlineKeyboardButton(">", callback_data=f"calendar_{country_code}_{next_year}_{next_month}"),
    ]

    # Days of the week
    days_buttons = [[InlineKeyboardButton(day, callback_data="ignore") for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]]]

    # Calendar days
    day_buttons = []
    for week in month_days:
        day_row = []
        for day in week:
            if day == 0:
                day_row.append(InlineKeyboardButton(" ", callback_data="ignore"))
            else:
                holiday_name = HOLIDAYS.get((month, day))
                if holiday_name:
                    button_text = f"🔴 {day}"
                    callback_data = f"holiday_{holiday_name}"
                else:
                    button_text = str(day)
                    callback_data = "ignore"

                if day == now.day and month == now.month and year == now.year:
                    button_text = f"🔵 {day}"

                day_row.append(InlineKeyboardButton(button_text, callback_data=callback_data))
        day_buttons.append(day_row)

    # Get the country name and flag emoji
    country = pycountry.countries.get(alpha_2=country_code)
    if not country:
        raise ValueError("Invalid country code")

    country_name = country.name
    flag_emoji = chr(0x1F1E6 + ord(country_code[0]) - ord('A')) + chr(0x1F1E6 + ord(country_code[1]) - ord('A'))

    # Get the time zone for the country
    time_zone = pytz.country_timezones.get(country_code)
    if not time_zone:
        raise ValueError("No time zone found for this country")

    tz = pytz.timezone(time_zone[0])
    now = datetime.now(tz)

    # Format the current time
    current_time = now.strftime("%I:%M:%S %p")

    # Combine everything
    keyboard = (
        [
            [InlineKeyboardButton(f"{calendar.month_name[month]} {year}", callback_data="ignore"),
             InlineKeyboardButton(f"{now.strftime('%d %b, %Y')}", callback_data="ignore")],
            [InlineKeyboardButton(f"📅 {flag_emoji}  {country_name} | {current_time}", callback_data="ignore")]
        ] + days_buttons + day_buttons + [navigation_buttons]
    )
    return InlineKeyboardMarkup(keyboard)


async def get_time_and_calendar(country_code):
    # Get the country name and flag emoji
    country = pycountry.countries.get(alpha_2=country_code)
    if not country:
        raise ValueError("Invalid country code")

    country_name = country.name
    flag_emoji = chr(0x1F1E6 + ord(country_code[0]) - ord('A')) + chr(0x1F1E6 + ord(country_code[1]) - ord('A'))

    # Get the time zone for the country
    time_zone = pytz.country_timezones.get(country_code)
    if not time_zone:
        raise ValueError("No time zone found for this country")

    tz = pytz.timezone(time_zone[0])
    now = datetime.now(tz)

    # Format the time and date
    time_str = now.strftime("%I:%M:%S %p")

    calendar_markup = await get_calendar_markup(now.year, now.month, country_code)

    return (
        f"📅 {flag_emoji} <b>{country_name} Calendar | ⏰ {time_str} 👇</b>",
        calendar_markup
    )

def setup_time_handler(app: Client):
    @app.on_message(filters.command("time", prefixes=["/", "."]) & (filters.private | filters.group))
    async def handle_time_command(client, message):
        if len(message.command) == 1:
            await message.reply_text(
                "<b>❌ Ensure you provide a valid country code.</b>",
                parse_mode=ParseMode.HTML,
            )
        else:
            country_code = message.command[1].upper()
            try:
                header_text, calendar_markup = await get_time_and_calendar(country_code)
                await message.reply_text(
                    header_text, parse_mode=ParseMode.HTML, reply_markup=calendar_markup
                )
            except Exception as e:
                await message.reply_text(
                    f"<b>Error:</b> {str(e)}", parse_mode=ParseMode.HTML
                )

    @app.on_callback_query(filters.regex(r'^(calendar_|holiday_)'))
    async def handle_calendar_callback(client, callback_query):
        if callback_query.data.startswith("calendar_"):
            _, country_code, year, month = callback_query.data.split("_")
            year = int(year)
            month = int(month)
            try:
                calendar_markup = await get_calendar_markup(year, month, country_code)
                await callback_query.message.edit_reply_markup(reply_markup=calendar_markup)
            except Exception as e:
                await callback_query.answer(f"Error: {str(e)}", show_alert=True)
        elif callback_query.data.startswith("holiday_"):
            holiday_name = callback_query.data.split("_", 1)[1]
            await callback_query.answer(holiday_name, show_alert=True)
        elif callback_query.data == "ignore":
            await callback_query.answer()
