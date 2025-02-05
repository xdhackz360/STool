from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode

# Define the inline keyboards for the menus
main_menu_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("AI Tools", callback_data="ai_tools"), InlineKeyboardButton("Credit Cards", callback_data="credit_cards")],
    [InlineKeyboardButton("Crypto", callback_data="crypto"), InlineKeyboardButton("Converter", callback_data="converter")],
    [InlineKeyboardButton("Decoders", callback_data="decoders"), InlineKeyboardButton("Downloaders", callback_data="downloaders")],
    [InlineKeyboardButton("Domain Check", callback_data="domain_check"), InlineKeyboardButton("Education Utils", callback_data="education_utils")],
    [InlineKeyboardButton("Github", callback_data="github"), InlineKeyboardButton("Info", callback_data="info")],
    [InlineKeyboardButton("Next ➡️", callback_data="next_1"), InlineKeyboardButton("Close ❌", callback_data="close")]
])

second_menu_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("Mail Tools", callback_data="mail_tools"), InlineKeyboardButton("Network Tools", callback_data="network_tools")],
    [InlineKeyboardButton("Random Address", callback_data="random_address"), InlineKeyboardButton("String Session", callback_data="string_session")],
    [InlineKeyboardButton("Stripe Keys", callback_data="stripe_keys"), InlineKeyboardButton("Sticker", callback_data="sticker")],
    [InlineKeyboardButton("Time Date", callback_data="time_date"), InlineKeyboardButton("Translate", callback_data="translate")],
    [InlineKeyboardButton("Tempmail", callback_data="tempmail"), InlineKeyboardButton("Text OCR", callback_data="text_ocr")],
    [InlineKeyboardButton("Previous ⬅️", callback_data="previous_1"), InlineKeyboardButton("Next ➡️", callback_data="next_2")],
    [InlineKeyboardButton("Close ❌", callback_data="close")]
])

third_menu_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("Web Capture", callback_data="web_capture"), InlineKeyboardButton("Yt Tools", callback_data="yt_tools")],
    [InlineKeyboardButton("Admin", callback_data="admin"),InlineKeyboardButton("Cricket", callback_data="cricket")],
    [InlineKeyboardButton("Previous ⬅️", callback_data="previous_2"),InlineKeyboardButton("Close ❌", callback_data="close")]
])

# Responses dictionary for different commands
responses = {
    "ai_tools": (
        "<b>🤖 AI Tools Commands</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "<b>USAGE:</b>\n"
        "Interact with AI for text-based queries and image analysis using these commands:\n\n"
        "➢ <b>/gpt [Question]</b> - Ask a question to ChatGPT 3.5.\n"
        "   - Example: <code>/gpt What is the capital of France?</code> (Returns the answer 'Paris')\n\n"
        "➢ <b>/gem [Question]</b> - Ask a question to Gemini AI.\n"
        "   - Example: <code>/gem How does photosynthesis work?</code> (Returns an explanation of photosynthesis)\n\n"
        "➢ <b>/imgai [Optional Prompt]</b> - Analyze an image or generate a response based on it.\n"
        "   - Basic Usage: Reply to an image with <code>/imgai</code> to get a general analysis.\n"
        "   - With Prompt: Reply to an image with <code>/imgai [Your Prompt]</code> to get a specific response.\n"
        "   - Example 1: Reply to an image with <code>/imgai</code> (Provides a general description of the image).\n"
        "   - Example 2: Reply to an image with <code>/imgai What is this?</code> (Provides a specific response based on the prompt and image).\n\n"
        ">NOTE:\n"
        "1️⃣ These tools leverage advanced AI models for accurate and detailed outputs.\n\n"
        ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
        ,
        {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
    ),
    "crypto": (
        "<b>💰 Cryptocurrency Commands</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "<b>USAGE:</b>\n"
        "Stay updated with real-time cryptocurrency data and market trends using these commands:\n\n"
        "➢ <b>/price [Token Name]</b> - Fetch real-time prices for a specific cryptocurrency.\n"
        "   - Example: <code>/price BTC</code> (Returns the current price of Bitcoin)\n\n"
        "➢ <b>/p2p</b> - Get the latest P2P trades for currency BDT (Bangladeshi Taka).\n"
        "   - Example: <code>/p2p</code> (Returns the latest P2P trade prices for cryptocurrencies in BDT)\n\n"
        "➢ <b>/gainers</b> - View cryptocurrencies with the highest price increases.\n"
        "   - Example: <code>/gainers</code> (Returns a list of top-performing cryptos with high price surges)\n\n"
        "➢ <b>/losers</b> - View cryptocurrencies with the largest price drops.\n"
        "   - Example: <code>/losers</code> (Returns a list of cryptos with significant price declines, indicating potential buying opportunities)\n\n"
        ">✨ NOTE:\n"
        "1️⃣ Data for prices, P2P trades, gainers, and losers is fetched in real-time using the Binance API.\n\n"
        ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
        ,
        {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
    ),
    "decoders": (
        "<b>🔤 Text and Encoding Tools Commands</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "<b>USAGE:</b>\n"
        "Perform encoding, decoding, text transformations, and word count using these commands:\n\n"
        "<b>Encoding and Decoding Commands:</b>\n"
        "➢ <b>/b64en [text]</b> - Base64 encode.\n"
        "   - Example: <code>/b64en Hello</code> (Encodes 'Hello' into Base64 format)\n"
        "➢ <b>/b64de [text]</b> - Base64 decode.\n"
        "   - Example: <code>/b64de SGVsbG8=</code> (Decodes 'SGVsbG8=' into 'Hello')\n"
        "➢ <b>/b32en [text]</b> - Base32 encode.\n"
        "   - Example: <code>/b32en Hello</code> (Encodes 'Hello' into Base32 format)\n"
        "➢ <b>/b32de [text]</b> - Base32 decode.\n"
        "   - Example: <code>/b32de JBSWY3DP</code> (Decodes 'JBSWY3DP' into 'Hello')\n"
        "➢ <b>/binen [text]</b> - Binary encode.\n"
        "   - Example: <code>/binen Hello</code> (Encodes 'Hello' into binary)\n"
        "➢ <b>/binde [text]</b> - Binary decode.\n"
        "   - Example: <code>/binde 01001000 01100101 01101100 01101100 01101111</code> (Decodes binary into 'Hello')\n"
        "➢ <b>/hexen [text]</b> - Hex encode.\n"
        "   - Example: <code>/hexen Hello</code> (Encodes 'Hello' into hexadecimal format)\n"
        "➢ <b>/hexde [text]</b> - Hex decode.\n"
        "   - Example: <code>/hexde 48656c6c6f</code> (Decodes '48656c6c6f' into 'Hello')\n"
        "➢ <b>/octen [text]</b> - Octal encode.\n"
        "   - Example: <code>/octen Hello</code> (Encodes 'Hello' into octal format)\n"
        "➢ <b>/octde [text]</b> - Octal decode.\n"
        "   - Example: <code>/octde 110 145 154 154 157</code> (Decodes '110 145 154 154 157' into 'Hello')\n\n"
        "<b>Text Transformation Commands:</b>\n"
        "➢ <b>/trev [text]</b> - Reverse text.\n"
        "   - Example: <code>/trev Hello</code> (Returns 'olleH')\n"
        "➢ <b>/tcap [text]</b> - Transform text to capital letters.\n"
        "   - Example: <code>/tcap hello</code> (Returns 'HELLO')\n"
        "➢ <b>/tsm [text]</b> - Transform text to small letters.\n"
        "   - Example: <code>/tsm HELLO</code> (Returns 'hello')\n\n"
        "<b>Word Count Command:</b>\n"
        "➢ <b>/wc [text]</b> - Count words in the given text.\n"
        "   - Example: <code>/wc Hello World!</code> (Returns 'Word Count: 2')\n\n"
        ">NOTE:\n"
        "1️⃣ Ensure text input is in a valid format for encoding and decoding commands.\n\n"
        ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
        ,
        {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
    ),
    "domain_check": (
        "<b>🌐 Domain Checker Commands</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "<b>USAGE:</b>\n"
        "Use the following command to check the registration status and availability of domains:\n\n"
        "➢ <b>/dmn [domain_name]</b> - Example: <code>/dmn google.com</code>\n\n"
        "<b>Multi-Domain Check:</b>\n"
        "You can check up to 20 domains at a time by separating them with spaces.\n"
        "Example: <code>/dmn google.com youtube.com demo.net</code>\n\n"
        ">NOTE:\n"
        "1️⃣ The maximum limit for a single check is 20 domains.\n\n"
        ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
        ,
        {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
    ),
    "github": (
        "<b>🤖 Github Tools Commands</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "<b>USAGE:</b>\n\n"
        "➢ <b>/git [url] [branch]</b> - Download Github Repository or Specific Branch.\n"
        "   - Example: <code>/git https://github.com/yt-dlp/yt-dlp master</code>\n"
        "   - Example: <code>/git https://github.com/abirxdhack/Chat-ID-Bot</code>\n\n"
        "<b>INSTRUCTIONS:</b>\n"
        "1. Use the <code>/git</code> command followed by a valid GitHub repository URL.\n"
        "2. Optionally, specify the branch name to download a specific branch.\n"
        "3. If no branch name is provided, the default branch of the repository will be downloaded.\n"
        "4. The repository will be downloaded as a ZIP file.\n"
        "5. The bot will send you the repository details and the file directly.\n\n"
        ">NOTE:\n"
        "1. Only public repositories are supported.\n"
        "2. Ensure the URL is formatted correctly.\n\n"
        ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
        ,
        {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
    ),
    "credit_cards": (
        "<b>💳 Credit Card Tools</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "<b>USAGE:</b>\n"
        "Perform credit card generation, validation, filtering, and scraping using these commands:\n\n"
        "➢ <b>/gen [BIN] [Amount]</b> - Generate credit card details using a BIN.\n"
        "   - Example 1: <code>/gen 460827</code> (Generates 10 CC details by default using BIN 460827)\n"
        "   - Example 2: <code>/gen 460827 100</code> (Generates 100 CC details using BIN 460827)\n\n"
        "➢ <b>/bin [BIN]</b> - Check and validate BIN details.\n"
        "   - Example: <code>/bin 460827</code> (Returns issuer, country, and card type details for the BIN 460827)\n\n"
        "➢ <b>/mbin [Text File or Message]</b> - Check up to 20 BINs at a time from a text file or message.\n"
        "   - Example: Reply to a message or a .txt file containing BINs and use <code>/mbin</code> to validate all.\n\n"
        "➢ <b>/scr [Chat Link or Username] [Amount]</b> - Scrape credit cards from a chat.\n"
        "   - Example: <code>/scr @abir_x_official 100</code> (Scrapes 100 CC details from the specified chat)\n"
        "   - Target BIN Example: <code>/scr @abir_x_official 100 460827 </code> (Scrapes 100 CC details with BIN 460827 from the chat)\n\n"
        "➢ <b>/fcc [File]</b> - Filter CC details from a file.\n"
        "   - Example: Reply to a .txt file containing CC details with <code>/fcc</code> to extract valid CC data.\n\n"
        "➢ <b>/extp [File or BIN]</b> - Extrapolate credit card data from a BIN.\n"
        "   - Example: <code>/extp 460827</code> (Generates extrapolated CC using BIN 460827)\n\n"
        "➢ <b>/mgen [BINs] [Amount]</b> - Generate CC details using multiple BINs.\n"
        "   - Example: <code>/mgen 460827,537637 10</code> (Generates 10 CC details for each BIN provided)\n\n"
        "➢ <b>/mc [Chat Link or Usernames] [Amount]</b> - Scrape CC details from multiple chats.\n"
        "   - Example: <code>/mc @abir_x_official_chat @ModVipRM_Discussion 200</code> (Scrapes 200 CC details from both chats)\n\n"
        "➢ <b>/topbin [File]</b> - Find the top 20 most used BINs from a combo.\n"
        "   - Example: Reply to a .txt file with <code>/topbin</code> to extract the top 20 BINs.\n\n"
        "➢ <b>/binbank [Bank Name]</b> - Find BIN database by bank name.\n"
        "   - Example: <code>/binbank Chase</code> (Returns BIN details for cards issued by Chase Bank)\n\n"
        "➢ <b>/bindb [Country Name]</b> - Find BIN database by country name.\n"
        "   - Example: <code>/bindb USA</code> (Returns BIN details for cards issued in the USA)\n\n"
        "➢ <b>/adbin [BIN]</b> - Filter specific BIN cards from a combo.\n"
        "   - Example: <code>/adbin 460827</code> (Filters CC details with BIN 460827 from a file or message)\n\n"
        "➢ <b>/rmbin [BIN]</b> - Remove specific BIN cards from a combo.\n"
        "   - Example: <code>/rmbin 460827</code> (Removes CC details with BIN 460827 from a file or message)\n\n"
        ">✨ NOTE:\n"
        "1️⃣ Always ensure compliance with legal and privacy regulations when using these tools.\n\n"
        ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
        ,
        {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
    ),
    "converter": (
        "<b>🎵 Audio Extraction Command</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "<b>USAGE:</b>\n"
        "Extract audio from a video using this command:\n\n"
        "➢ <b>/aud</b> - Reply to a video message with this command to convert the video into audio.\n\n"
        ">NOTE:\n"
        "1️⃣ Ensure you reply directly to a video message with the <code>/aud</code> command.\n"
        "2️⃣ The extracted audio will be provided in a standard format (e.g., MP3).\n\n"
        ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
        ,
        {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
    ),
    "downloaders": (
        "<b>🎥 Social Media and Music Downloader</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "<b>USAGE:</b>\n"
        "Download videos and tracks from popular platforms using these commands:\n\n"
        "➢ <b>/fb [Video URL]</b> - Download a Facebook video.\n"
        "   - Example: <code>/fb https://www.facebook.com/share/v/18VH1yNXoq/</code> (Downloads the specified Facebook video)\n"
        "   - Note: Private Facebook videos cannot be downloaded.\n\n"
        "➢ <b>/pin [Video URL]</b> - Download a Pinterest video.\n"
        "   - Example: <code>/pin https://pin.it/6GoDMRwmE</code> (Downloads the specified Pinterest video)\n\n"
        "➢ <b>/in [Video URL]</b> - Download Instagram Reels.\n"
        "   - Example: <code>/in https://www.instagram.com/reel/C_vOYErJBm7/?igsh=YzljYTk1ODg3Zg==</code> (Downloads the specified Instagram reel)\n"
        "   - Note: 18+ Instagram Reels cannot be downloaded.\n\n"
        "➢ <b>/sp [Track URL]</b> - Download a Spotify track.\n"
        "   - Example: <code>/sp https://open.spotify.com/track/7ouBSPZKQpm7zQz2leJXta</code> (Downloads the specified Spotify track)\n\n"
        "➢ <b>/yt [Video URL]</b> - Download a YouTube video.\n"
        "   - Example: <code>/yt https://youtu.be/In8bfGnXavw</code> (Downloads the specified YouTube video)\n\n"
        "➢ <b>/song [Video URL]</b> - Download a YouTube video as an MP3 file.\n"
        "   - Example: <code>/song https://youtu.be/In8bfGnXavw</code> (Converts and downloads the video as MP3)\n\n"
        ">NOTE:\n"
        "1️⃣ Provide a valid public URL for each platform to download successfully.\n\n"
        ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
        ,
        {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
    ),
"education_utils": (
            "<b>📚 Language Tools Commands</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "<b>USAGE:</b>\n"
            "Enhance your language skills with these commands for fixing spelling, grammar, checking synonyms, antonyms, and pronunciations:\n\n"
            "➢ <b>/spell [Word]</b> - Correct the spelling of a word.\n"
            "   - Example: <code>/spell teh</code> (Returns the corrected spelling: 'the')\n"
            "   - Reply Example: Reply to a message with <code>/spell</code> to correct the spelling of a specific word.\n\n"
            "➢ <b>/gra [Sentence]</b> - Fix grammatical issues in a sentence.\n"
            "   - Example: <code>/gra I has a book</code> (Returns the corrected sentence: 'I have a book')\n"
            "   - Reply Example: Reply to a message with <code>/gra</code> to fix grammatical errors in the sentence.\n\n"
            "➢ <b>/syn [Word]</b> - Check synonyms and antonyms for a given word.\n"
            "   - Example: <code>/syn happy</code> (Returns synonyms like 'joyful' and antonyms like 'sad')\n\n"
            "➢ <b>/prn [Word]</b> - Check the pronunciation of a word.\n"
            "   - Example: <code>/prn epitome</code> (Returns the pronunciation in phonetic format or audio: 'eh-pit-uh-mee')\n\n"
            ">NOTE:\n"
            "1️⃣ These tools support common English words and sentences.\n"
            "2️⃣ Ensure the word or sentence provided is clear for accurate results.\n"
            "3️⃣ Reply to a message with the command to apply it directly to the text in the message.\n\n"
            ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
            ,
            {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
        ),
        "info": (
            "<b>ℹ️ Info Command</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "<b>USAGE:</b>\n"
            "Retrieve detailed information about any user, group, or channel using this command:\n\n"
            "➢ <b>/info [target]</b> - Example: <code>/info @abirxdhackz</code> or <code>/info 7303810912</code>\n\n"
            ">NOTE:\n"
            "1️⃣ For groups/channels, use their username or numeric ID.\n"
            "2️⃣ Ensure proper input format to get accurate results.\n\n"
            ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
            ,
            {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
        ),
        "mail_tools": (
            "<b>📋 Email and Credential Commands</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "<b>USAGE:</b>\n"
            "Extract and scrape emails or email-password pairs using these commands:\n\n"
            "➢ <b>/fmail</b> - Filter or extract emails by replying to a message or a text file.\n"
            "   - Example: Reply to a message containing text or a .txt file and use <code>/fmail</code> to extract all emails.\n\n"
            "➢ <b>/fpass</b> - Filter or extract email-password pairs by replying to a message or a text file.\n"
            "   - Example: Reply to a message containing credentials or a .txt file and use <code>/fpass</code> to extract all email-password pairs.\n\n"
            "➢ <b>/scrmail [Chat Username/Link] [Amount]</b> - Scrape email-password pairs from a Telegram group or channel.\n"
            "   - Example: <code>/scrmail @abir_x_official 100</code> (Scrapes the first 100 messages from the specified group or channel for email-password pairs)\n\n"
            ">NOTE:\n"
            "1️⃣ For <code>/scrmail</code>, provide the chat username or link (e.g., <code>@ChatName</code> or <code>https://t.me/ChatName</code>) and the number of messages to scrape.\n"
            "2️⃣ Ensure that the chat username or link provided is valid and accessible.\n"
            "3️⃣ These tools are intended for data filtering and scraping; ensure compliance with privacy and legal regulations.\n\n"
            ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
            ,
            {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
        ),
        "random_address": (
            "<b>🏠 Random Address Generator</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "<b>USAGE:</b>\n"
            "Generate random fake addresses for specific countries or regions:\n\n"
            "➢ <b>/fake [Country Code or Country Name]</b> - Generates a random address for the specified country.\n"
            "   - Example: <code>/fake BD</code> or <code>/fake Bangladesh</code>\n\n"
            "<b>Alternative Command:</b>\n"
            "➢ <b>/rnd [Country Code or Country Name]</b> - Works the same as <code>/fake</code>.\n\n"
            ">NOTE:\n"
            "1️⃣ Supported formats include either the country code (e.g., <code>US</code>, <code>BD</code>) or full country name (e.g., <code>UnitedStates</code>, <code>Bangladesh</code>).\n"
            "2️⃣ Some countries may not have address data available.\n\n"
            ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
            ,
            {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
        ),
        "stripe_keys": (
            "<b>💳 Stripe Key Commands</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "<b>USAGE:</b>\n"
            "Verify and retrieve information about Stripe keys using these commands:\n\n"
            "➢ <b>/sk [Stripe Key]</b> - Check whether the provided Stripe key is live or dead.\n"
            "   - Example: <code>/sk sk_live_4eC39HqLyjWDarjtT1zdp7dc</code> (Verifies the given Stripe key)\n\n"
            "➢ <b>/skinfo [Stripe Key]</b> - Retrieve detailed information about the provided Stripe key.\n"
            "   - Example: <code>/skinfo sk_live_4eC39HqLyjWDarjtT1zdp7dc</code> (Fetches details like account type, region, etc.)\n\n"
            ">NOTE:\n"
            "1️⃣ Ensure you provide a valid Stripe key for both commands.\n\n"
            ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
            ,
            {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
        ),
        "time_date": (
            "<b>🕒 Time Command</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "<b>USAGE:</b>\n"
            "Get the current time and date for any country using this command:\n\n"
            "➢ <b>/time [Country Code]</b> - Fetch the current time and date of the specified country.\n"
            "   - Example: <code>/time US</code> or <code>/time BD</code>\n\n"
            ">NOTE:\n"
            "1️⃣ Use valid country codes (e.g., <code>US</code> for the United States, <code>BD</code> for Bangladesh).\n\n"
            ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
            ,
            {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
        ),
        "tempmail": (
            "<b>📧 Temporary Mail Tools</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "<b>USAGE:</b>\n"
            "Generate and manage temporary emails using these commands:\n\n"
            "➢ <b>/tmail</b> - Generate a random temporary email with a password.\n"
            "   - Example: <code>/tmail</code> (Creates a random email and generates a unique password)\n\n"
            "➢ <b>/tmail [username]:[password]</b> - Generate a specific temporary email with your chosen username and password.\n"
            "   - Example: <code>/tmail user123:securePass</code> (Creates <code>user123@temp.com</code> with the password <code>securePass</code>)\n\n"
            "➢ <b>/cmail [mail token]</b> - Check the most recent 10 emails received by your temporary mail.\n"
            "   - Example: <code>/cmail abc123token</code> (Displays the last 10 mails for the provided token)\n\n"
            ">✨ NOTE:\n"
            "1️⃣ When generating an email, a unique mail token is provided. This token is required to check received emails.\n"
            "2️⃣ Each email has a different token, so keep your tokens private to prevent unauthorized access.\n\n"
            ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
            ,
            {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
        ),
        "network_tools": (
            "<b>🌐 Network Tool Commands</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "<b>USAGE:</b>\n"
            "Utilize these commands to gather IP-related information and check HTTP/HTTPS proxies:\n\n"
            "➢ <b>/ip [IP Address]</b> - Get detailed information about a specific IP address.\n"
            "   - Example: <code>/ip 8.8.8.8</code>\n\n"
            "➢ <b>/px [Proxy/Proxies]</b> - Check the validity and status of HTTP/HTTPS proxies.\n"
            "   - Single Proxy Example: <code>/px 192.168.0.1:8080</code>\n"
            "   - With Authentication: <code>/px 192.168.0.1:8080 user password</code>\n"
            "   - Multiple Proxies Example: <code>/px 192.168.0.1:8080 10.0.0.2:3128 172.16.0.3:8080 user password</code>\n\n"
            ">NOTE:\n"
            "1️⃣ For <code>/ip</code>, ensure the input is a valid IP address.\n"
            "2️⃣ For <code>/px</code>, proxies can be provided in either <code>[IP:Port]</code> or <code>[IP:Port User Pass]</code> formats.\n\n"
            ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
            ,
            {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
        ),
        "string_session": (
            "<b>🔑 Telegram String Session Generator</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "<b>USAGE:</b>\n"
            "Generate string sessions for managing Telegram accounts programmatically using these commands:\n\n"
            "➢ <b>/pyro</b> - Generate a Pyrogram Telegram string session.\n"
            "   - Example: <code>/pyro</code> (Starts the process to generate a Pyrogram string session)\n\n"
            "➢ <b>/tele</b> - Generate a Telethon Telegram string session.\n"
            "   - Example: <code>/tele</code> (Starts the process to generate a Telethon string session)\n\n"
            ">NOTE:\n"
            "1️⃣ Pyrogram and Telethon are Python libraries for interacting with Telegram APIs.\n"
            "2️⃣ Use <code>/pyro</code> for Pyrogram-based projects and <code>/tele</code> for Telethon-based projects.\n"
            "3️⃣ Follow the prompts to enter your Telegram login credentials securely. Keep the generated session string private.\n\n"
            ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
            ,
            {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
        ),
        "sticker": (
            "<b>🎨 Sticker Commands</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "<b>USAGE:</b>\n"
            "Easily create or customize stickers with these commands:\n\n"
            "➢ <b>/q</b> - Generate a sticker from any text message.\n"
            "   - Example: Reply to any text message in the chat with <code>/q</code> to convert it into a sticker.\n\n"
            "➢ <b>/kang</b> - Add any image, sticker, or animated sticker to your personal sticker pack.\n"
            "   - Example: Reply to an image, sticker, or animated sticker with <code>/kang</code> to add it to your pack.\n\n"
            ">NOTE:\n"
            "1️⃣ For <code>/q</code>, ensure you reply directly to a text message to generate the sticker.\n"
            "2️⃣ For <code>/kang</code>, reply directly to the media or sticker you want to add to your pack.\n\n"
            ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
            ,
            {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
        ),
"translate": (
    "<b>🌐 Translation Commands</b>\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n"
    "<b>USAGE:</b>\n"
    "Translate text into various languages using these commands:\n\n"
    "➢ <b>/tr [Language Code] [Text]</b> - Translate the given text into the specified language.\n"
    "   - Example: <code>/tr es Hello!</code> (Translates 'Hello!' to Spanish)\n"
    "   - Reply Example: Reply to any message with <code>/tres</code> to translate it into Spanish.\n\n"
    "➢ <b>/tr en [Text]</b> - Translate the given text into English.\n"
    "   - Example: <code>/tr en Hola!</code> (Translates 'Hola!' to English)\n"
    "   - Reply Example: Reply to any message with <code>/tr en</code> to translate it into English.\n\n"
    "➢ <b>/tr bn [Text]</b> - Translate the given text into Bengali.\n"
    "   - Example: <code>/tr bn Hello!</code> (Translates 'Hello!' to Bengali)\n"
    "   - Reply Example: Reply to any message with <code>/tr bn</code> to translate it into Bengali.\n\n"
    "<b>NOTE:</b>\n"
    "1️⃣ Use the <code>/tr[Language Code]</code> format for translation, where <code>[Language Code]</code> specifies the target language (e.g., <code>es</code> for Spanish, <code>fr</code> for French).\n"
    "2️⃣ Supported commands include <code>/tr en</code> (English), <code>/tr bn</code> (Bengali), <code>/tr hi</code> (Hindi), and others.\n"
    "3️⃣ To translate, either type the text with the command or reply to a message with the command.\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n"
    "🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
    ,
    {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
        ),
        "text_ocr": (
            "<b>🔍 OCR Command</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "<b>USAGE:</b>\n"
            "Extract English text from an image using this command:\n\n"
            "➢ <b>/ocr</b> - Reply to an image with this command to extract readable English text from it.\n\n"
            ">NOTE:\n"
            "1️⃣ This command only works with clear images containing English text.\n"
            "2️⃣ Ensure the image is not blurry or distorted for accurate text extraction.\n\n"
            ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
            ,
            {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
        ),
        "web_capture": (
            "<b>🌐 Web Tools Commands</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "<b>USAGE:</b>\n"
            "Perform webpage-related tasks like taking screenshots or downloading source code using these commands:\n\n"
            "➢ <b>/ss [Website URL]</b> - Take a screenshot of the specified webpage.\n"
            "   - Example: <code>/ss https://example.com</code> (Captures a screenshot of the given website)\n\n"
            "➢ <b>/ws [Website URL]</b> - Download the HTML source code of the specified webpage.\n"
            "   - Example: <code>/ws https://example.com</code> (Downloads the source code of the given website)\n\n"
            ">NOTE:\n"
            "1️⃣ Ensure you provide a valid and accessible website URL for both commands.\n\n"
            ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
            ,
            {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
        ),
        "yt_tools": (
            "<b>🎥 YouTube Tools Commands</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "<b>USAGE:</b>\n"
            "Easily extract tags or download thumbnails from YouTube videos using these commands:\n\n"
            "➢ <b>/ytag [YouTube Video URL]</b> - Extract all tags from a YouTube video.\n"
            "   - Example: <code>/ytag https://youtu.be/In8bfGnXavw</code> (Fetches tags for the specified video)\n\n"
            "➢ <b>/yth [YouTube Video URL]</b> - Download the thumbnail of a YouTube video.\n"
            "   - Example: <code>/yth https://youtu.be/In8bfGnXavw</code> (Downloads the thumbnail of the specified video)\n\n"
            ">NOTE:\n"
            "1️⃣ Ensure you provide a valid YouTube video URL with the commands.\n\n"
            ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
            ,
            {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
        ),
    "about_me": (
        "<b>Name:</b> Smart Tool ⚙️\n"
        "<b>Version:</b> 3.0 (Beta Testing) 🛠\n\n"
        "<b>Development Team:</b>\n"
        "- <b>Creator:</b> <a href='https://t.me/abirxdhackz'>⏤͟͞〲ᗩᗷiᖇ 𓊈乂ᗪ𓊉 👨‍💻</a>\n"
        "<b>Technical Stack:</b>\n"
        "- <b>Language:</b> Python 🐍\n"
        "- <b>Libraries:</b> Aiogram, Pyrogram And Telethon 📚\n"
        "- <b>Database:</b> MongoDB Database 🗄\n"
        "- <b>Hosting:</b> Hostinger VPS 🌐\n\n"
        "<b>About:</b> Smart Tool ⚙️ The ultimate Telegram toolkit! Education, AI, downloaders, temp mail, finance tools & more—simplify life!\n\n"
        ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
        ,
        {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
    ),
"admin": (
    "<b>🚫 Ban, Unban, Mute, and Unmute Commands</b>\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n"
    "<b>USAGE:</b>\n"
    "Manage user bans and mutes in the group using these commands:\n\n"
    "➢ <b>/ban</b> with username or userid - For Ban a user from the group.\n"
    "➢ <b>/fuck</b> with username or userid - For Ban a user from the group.\n"
    "➢ <b>/unban</b> with username or userid - For unban a user from the group.\n"
    "➢ <b>/unfuck</b> with username or userid - For unban a user from the group.\n"
    "➢ <b>/ban</b> with multiple usernames or user IDs - For Multi Ban from the group.\n"
    "➢ <b>/unban</b> with multiple usernames or user IDs - For Multi unban from the group.\n"
    "➢ <b>/mute</b> with username or userid - For mute a user in the group (they can’t send messages).\n"
    "➢ <b>/unmute</b> with username or userid - For unmute a user in the group (they can send messages again).\n"
    "➢ <b>/mute</b> with multiple usernames or user IDs - For Multi mute in the group.\n"
    "➢ <b>/unmute</b> with multiple usernames or user IDs - For Multi unmute in the group.\n\n"
    ">NOTE:\n"
    "1️⃣ Ensure you have the necessary permissions to ban/unban/mute/unmute users in the group.\n"
    "2️⃣ Use the commands in group chats only.\n\n"
    ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
,
    {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
    ),
    "cricket": (
    "<b>🏏 Smart-Tool Cricket Score Commands</b>\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n"
    "<b>USAGE:</b>\n"
    "Get recent and real-time cricket score updates using these commands:\n\n"
    "➢ <b>/matches</b> - Command for Recent/Running Cricket Match list.\n"
    "➢ <b>/score [match id]</b> - For Getting Realtime Cricket Score Update.\n\n"
    "✨ <b>Note:</b>\n"
    "To get match_id, use the /matches command or visit cricbuzz.com and open a match URL to copy the match_id from the URL. Each match has a unique match_id. To get ICC Cricket World Cup 2023 match_id, use the /matches command.\n\n"
    ">🔔 For Bot Update News: <a href='https://t.me/ModVipRM'>Join Now</a>"
    ,
    {'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}
    )
}
async def handle_callback_query(client, callback_query):
    call = callback_query

    if call.data in responses:
        # Determine which keyboard to use for the back button based on the current menu
        if call.data == "about_me":
            back_button = InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="start_message")]
            ])
        elif call.data in ["ai_tools", "credit_cards", "crypto", "converter", "decoders", "downloaders", "domain_check", "education_utils", "github", "info"]:
            back_button = InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]
            ])
        elif call.data in ["mail_tools", "network_tools", "random_address", "string_session", "stripe_keys", "sticker", "time_date", "translate", "tempmail", "text_ocr"]:
            back_button = InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="second_menu")]
            ])
        elif call.data in ["web_capture", "yt_tools", "cricket", "admin"]:
            back_button = InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="third_menu")]
            ])
        else:
            back_button = InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]
            ])

        await call.message.edit_text(
            responses[call.data][0],  # text is the first element in the tuple
            parse_mode=responses[call.data][1]['parse_mode'],
            disable_web_page_preview=responses[call.data][1]['disable_web_page_preview'],
            reply_markup=back_button
        )
    elif call.data == "main_menu":
        await call.message.edit_text(
            "<b>Here are the Smart Tool ⚙️ Options:</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=main_menu_keyboard
        )
    elif call.data == "next_1":
        await call.message.edit_text(
            "<b>Here are the Smart Tool ⚙️ Options:</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=second_menu_keyboard
        )
    elif call.data == "next_2":
        await call.message.edit_text(
            "<b>Here are the Smart Tool ⚙️ Options:</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=third_menu_keyboard
        )
    elif call.data == "previous_1":
        await call.message.edit_text(
            "<b>Here are the Smart Tool ⚙️ Options:</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=main_menu_keyboard
        )
    elif call.data == "previous_2":
        await call.message.edit_text(
            "<b>Here are the Smart Tool ⚙️ Options:</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=second_menu_keyboard
        )
    elif call.data == "close":
        await call.message.delete()
    elif call.data == "start_message":
        full_name = f"{call.message.from_user.first_name} {call.message.from_user.last_name}" if call.message.from_user.last_name else call.message.from_user.first_name

        # Main welcome message
        start_message = (
            f"<b>Hi {full_name}! Welcome To This Bot</b>\n"
            "<b>━━━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"
            "<b><a href='tg://user?id=7303810912'>Smart Tool ⚙️</a></b>: The ultimate toolkit on Telegram, offering education, AI, downloaders, temp mail, credit card tool, and more. Simplify your tasks with ease!\n"
            "<b>━━━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"
            "<b>Don't Forget To <a href='https://t.me/ModVipRM'>Join Here</a> For Updates!</b>"
        )
        await call.message.edit_text(
            start_message,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⚙️ Main Menu", callback_data="main_menu"),
                 InlineKeyboardButton("➕ Add Me", url="https://t.me/ItsSmartToolBot?startgroup=new&admin=post_messages+delete_messages+edit_messages+pin_messages+change_info+invite_users+promote_members")],
                [InlineKeyboardButton("🔄 Updates", url="https://t.me/ModVipRM"),
                 InlineKeyboardButton("ℹ️ About Me", callback_data="about_me")]
            ]),
            disable_web_page_preview=True,
        )
    elif call.data == "second_menu":
        await call.message.edit_text(
            "<b>Here are the Smart Tool ⚙️ Options:</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=second_menu_keyboard
        )
    elif call.data == "third_menu":
        await call.message.edit_text(
            "<b>Here are the Smart Tool ⚙️ Options:</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=third_menu_keyboard
        )
