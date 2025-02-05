import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from asyncio import sleep
import pycountry
from faker import Faker

# Initialize Faker
fake = Faker()

# Special information for specific countries
special_addresses = {
    "DZ": {
        "street": "20 centre Culturel 99 Islamique",
        "postal_code": "02000",
        "city": "Chlef",
        "country": "Algeria"
    },
    "KZ": {
        "street": "IND,0062",
        "postal_code": "020101",
        "city": "Semipalatinsk",
        "country": "Kazakhstan"
    },
    "BD": {
        "street": "বিল্ডিং নং ৯৯৯, পশ্চিম হরিরামমহাসড়ক",
        "postal_code": "৬৪৪৯",
        "city": "নড়াইল",
        "country": "বাংলাদেশ"
    }
}

# Dictionary of phone number formats by country code
phone_formats = {
    "AF": "+93 70XXXXXXX",
    "AL": "+355 67XXXXXXX",
    "DZ": "+213 55XXXXXXX",
    "AR": "+54 911XXXXXXXX",
    "AU": "+61 41XXXXXXX",
    "AT": "+43 650XXXXXXX",
    "BD": "+880 18XXXXXXXX",
    "BE": "+32 49XXXXXXX",
    "BR": "+55 119XXXXXXXX",
    "CA": "+1 416XXXXXXX",
    "CN": "+86 13XXXXXXXXX",
    "CO": "+57 321XXXXXXX",
    "DK": "+45 20XXXXXX",
    "EG": "+20 100XXXXXXX",
    "FR": "+33 6XXXXXXXX",
    "DE": "+49 15XXXXXXXXX",
    "GR": "+30 69XXXXXXXX",
    "IN": "+91 91XXXXXXXX",
    "ID": "+62 81XXXXXXXXX",
    "IR": "+98 91XXXXXXXX",
    "IE": "+353 85XXXXXXX",
    "IL": "+972 50XXXXXXX",
    "IT": "+39 33XXXXXXXX",
    "JP": "+81 80XXXXXXXX",
    "KZ": "+7 70XXXXXXXX",
    "KE": "+254 71XXXXXXX",
    "MY": "+60 12XXXXXXXX",
    "MX": "+52 12XXXXXXXXX",
    "NP": "+977 98XXXXXXXX",
    "NL": "+31 6XXXXXXXX",
    "NZ": "+64 21XXXXXXX",
    "NG": "+234 70XXXXXXXX",
    "PK": "+92 3XXXXXXXXX",
    "PH": "+63 917XXXXXXX",
    "PL": "+48 51XXXXXXX",
    "PT": "+351 91XXXXXXX",
    "RU": "+7 91XXXXXXXX",
    "SA": "+966 50XXXXXXX",
    "SG": "+65 81XXXXXX",
    "ZA": "+27 72XXXXXXX",
    "KR": "+82 10XXXXXXXX",
    "ES": "+34 6XXXXXXXX",
    "LK": "+94 71XXXXXXX",
    "SE": "+46 70XXXXXXX",
    "CH": "+41 79XXXXXXX",
    "TH": "+66 81XXXXXXX",
    "TR": "+90 53XXXXXXXX",
    "UA": "+380 50XXXXXXX",
    "AE": "+971 50XXXXXXX",
    "GB": "+44 79XXXXXXXX",
    "US": "+1 202XXXXXXX",
    "VN": "+84 91XXXXXXX"
}

# List of available locales
locales = [
    "ar_EG", "ar_JO", "ar_SA", "at_AT", "bg_BG", "bn_BD",
    "cs_CZ", "da_DK", "de_AT", "de_CH", "de_DE", "el_CY",
    "el_GR", "en_AU", "en_CA", "en_GB", "en_HK", "en_IN",
    "en_NG", "en_NZ", "en_PH", "en_SG", "en_UG", "en_US",
    "en_ZA", "es_AR", "es_ES", "es_PE", "es_VE", "et_EE",
    "fa_IR", "fi_FI", "fr_BE", "fr_CA", "fr_CH", "fr_FR",
    "he_IL", "hr_HR", "hu_HU", "hy_AM", "id_ID", "is_IS",
    "it_CH", "it_IT", "ja_JP", "ka_GE", "kk_KZ", "ko_KR",
    "lt_LT", "lv_LV", "me_ME", "mn_MN", "ms_MY", "nb_NO",
    "ne_NP", "nl_BE", "nl_NL", "pl_PL", "pt_BR", "pt_PT",
    "ro_MD", "ro_RO", "ru_RU", "sk_SK", "sl_SI", "sr_Cyrl_RS",
    "sr_Latn_RS", "sr_RS", "sv_SE", "th_TH", "tr_TR", "uk_UA",
    "vi_VN", "zh_CN", "zh_TW"
]

def get_locale_for_country(alpha_2):
    locale = f"{alpha_2.lower()}_{alpha_2.upper()}"
    if locale in locales:
        return locale
    return None

def setup_fake_handler(app: Client):
    @app.on_message(filters.command(["fake", "rnd"], prefixes=["/", "."]) & (filters.private | filters.group))
    async def fake_handler(client: Client, message: Message):
        if len(message.command) <= 1:
            await message.reply_text("**❌ Provide a valid country name or country code.**")
            return
        
        country_code = message.command[1].upper()
        country = pycountry.countries.get(alpha_2=country_code) or pycountry.countries.get(name=country_code)
        
        if not country:
            await message.reply_text("**❌ Provide a valid country name or country code.**")
            return

        # Check if the country has special address information
        if country.alpha_2 in special_addresses:
            special_address = special_addresses[country.alpha_2]
            fake_address = {
                "full_name": fake.name(),
                "gender": fake.random_element(elements=("Male", "Female", "Other")),
                "street": special_address["street"],
                "city": special_address["city"],
                "state": "N/A",
                "postal_code": special_address["postal_code"],
                "phone_number": generate_phone_number(phone_formats[country.alpha_2]),
                "country_name": special_address["country"]
            }
        else:
            # Fetch fake address from API for other countries
            locale = get_locale_for_country(country.alpha_2) or f"{country.alpha_2.lower()}_{country.alpha_2.upper()}"
            api_url = f"https://fakerapi.it/api/v2/addresses?_quantity=1&_locale={locale}&_country_code={country.alpha_2}"
            response = requests.get(api_url)
            
            if response.status_code != 200:
                await message.reply_text("**❌ Failed to fetch fake address. Try again later.**")
                return

            data = response.json()['data'][0]

            # Parse the API response correctly
            fake_address = {
                "full_name": fake.name(),
                "gender": fake.random_element(elements=("Male", "Female", "Other")),
                "street": data.get('street', 'N/A'),
                "city": data.get('city', 'N/A'),
                "state": "N/A",
                "postal_code": data.get('zipcode', 'N/A'),
                "phone_number": generate_phone_number(phone_formats.get(country.alpha_2, "+XXXXXXXXXXX")),
                "country_name": data.get('country', 'N/A')
            }
        
        generating_message = await message.reply_text(f"**⚡️Generating Fake Address For {fake_address['country_name']}...⏳**")
        await sleep(2)
        await generating_message.delete()
        
        await message.reply_text(f"""
**Address for {fake_address['country_name']}:**
━━━━━━━━━━━━━━━━━
**Full Name:** `{fake_address['full_name']}`
**Gender:** `{fake_address['gender']}`
**Street:** `{fake_address['street']}`
**City/Town/Village:** `{fake_address['city']}`
**State/Province/Region:** `{fake_address['state']}`
**Postal code:** `{fake_address['postal_code']}`
**Phone Number:** `{fake_address['phone_number']}`
**Country:** `{fake_address['country_name']}`
""", parse_mode=ParseMode.MARKDOWN)

def generate_phone_number(phone_format):
    """
    Generate a phone number based on the country phone format.
    """
    phone_number = phone_format
    for _ in range(phone_number.count('X')):
        phone_number = phone_number.replace('X', str(fake.random_digit()), 1)
    return phone_number
