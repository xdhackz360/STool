# Smart Tool ⚙️ - The Ultimate Telegram Toolkit

Welcome to **Smart Tool ⚙️**! This Telegram bot is designed to simplify your digital life with a wide range of features, from educational tools and AI interactions to downloaders and finance tools. Whether you're looking to analyze text, download media, or generate temporary emails, Smart Tool ⚙️ has got you covered!

## Features

### 🤖 AI Tools Commands
Interact with AI for text-based queries and image analysis using these commands:
- **/gpt [Question]**: Ask a question to ChatGPT 3.5.
  - Example: `/gpt What is the capital of France?` (Returns the answer 'Paris')
- **/gem [Question]**: Ask a question to Gemini AI.
  - Example: `/gem How does photosynthesis work?` (Returns an explanation of photosynthesis)
- **/imgai [Optional Prompt]**: Analyze an image or generate a response based on it.
  - Basic Usage: Reply to an image with `/imgai` to get a general analysis.
  - With Prompt: Reply to an image with `/imgai [Your Prompt]` to get a specific response.
  - Example 1: Reply to an image with `/imgai` (Provides a general description of the image).
  - Example 2: Reply to an image with `/imgai What is this?` (Provides a specific response based on the prompt and image).

### 💰 Cryptocurrency Commands
Stay updated with real-time cryptocurrency data and market trends:
- **/price [Token Name]**: Fetch real-time prices for a specific cryptocurrency.
  - Example: `/price BTC` (Returns the current price of Bitcoin)
- **/p2p**: Get the latest P2P trades for currency BDT.
  - Example: `/p2p` (Returns the latest P2P trade prices for cryptocurrencies in BDT)
- **/gainers**: View cryptocurrencies with the highest price increases.
  - Example: `/gainers` (Returns a list of top-performing cryptos with high price surges)
- **/losers**: View cryptocurrencies with the largest price drops.
  - Example: `/losers` (Returns a list of cryptos with significant price declines, indicating potential buying opportunities)

### 🔤 Text and Encoding Tools Commands
Perform encoding, decoding, text transformations, and word count:
- **Encoding and Decoding Commands**:
  - **/b64en [text]**: Base64 encode.
    - Example: `/b64en Hello` (Encodes 'Hello' into Base64 format)
  - **/b64de [text]**: Base64 decode.
    - Example: `/b64de SGVsbG8=` (Decodes 'SGVsbG8=' into 'Hello')
  - **/b32en [text]**: Base32 encode.
    - Example: `/b32en Hello` (Encodes 'Hello' into Base32 format)
  - **/b32de [text]**: Base32 decode.
    - Example: `/b32de JBSWY3DP` (Decodes 'JBSWY3DP' into 'Hello')
  - **/binen [text]**: Binary encode.
    - Example: `/binen Hello` (Encodes 'Hello' into binary)
  - **/binde [text]**: Binary decode.
    - Example: `/binde 01001000 01100101 01101100 01101100 01101111` (Decodes binary into 'Hello')
  - **/hexen [text]**: Hex encode.
    - Example: `/hexen Hello` (Encodes 'Hello' into hexadecimal format)
  - **/hexde [text]**: Hex decode.
    - Example: `/hexde 48656c6c6f` (Decodes '48656c6c6f' into 'Hello')
  - **/octen [text]**: Octal encode.
    - Example: `/octen Hello` (Encodes 'Hello' into octal format)
  - **/octde [text]**: Octal decode.
    - Example: `/octde 110 145 154 154 157` (Decodes '110 145 154 154 157' into 'Hello')

- **Text Transformation Commands**:
  - **/trev [text]**: Reverse text.
    - Example: `/trev Hello` (Returns 'olleH')
  - **/tcap [text]**: Transform text to capital letters.
    - Example: `/tcap hello` (Returns 'HELLO')
  - **/tsm [text]**: Transform text to small letters.
    - Example: `/tsm HELLO` (Returns 'hello')

- **Word Count Command**:
  - **/wc [text]**: Count words in the given text.
    - Example: `/wc Hello World!` (Returns 'Word Count: 2')

### 🌐 Domain Checker Commands
Check the registration status and availability of domains:
- **/dmn [domain_name]**: Example: `/dmn google.com`
- **Multi-Domain Check**: You can check up to 20 domains at a time by separating them with spaces.
  - Example: `/dmn google.com youtube.com demo.net`

### 🤖 Github Tools Commands
Download GitHub repositories or specific branches:
- **/git [url] [branch]**: Download a GitHub repository or specific branch.
  - Example: `/git https://github.com/yt-dlp/yt-dlp master`
  - Example: `/git https://github.com/abirxdhack/Chat-ID-Bot`

### 💳 Credit Card Tools
Perform credit card generation, validation, filtering, and scraping:
- **/gen [BIN] [Amount]**: Generate credit card details using a BIN.
  - Example: `/gen 460827` (Generates 10 CC details by default using BIN 460827)
  - Example: `/gen 460827 100` (Generates 100 CC details using BIN 460827)
- **/bin [BIN]**: Check and validate BIN details.
  - Example: `/bin 460827` (Returns issuer, country, and card type details for the BIN 460827)
- **/mbin [Text File or Message]**: Check up to 20 BINs at a time from a text file or message.
  - Example: Reply to a message or a .txt file containing BINs and use `/mbin` to validate all.
- **/scr [Chat Link or Username] [Amount]**: Scrape credit cards from a chat.
  - Example: `/scr @abir_x_official 100` (Scrapes 100 CC details from the specified chat)
  - Target BIN Example: `/scr @abir_x_official 460827 100` (Scrapes 100 CC details with BIN 460827 from the chat)
- **/fcc [File]**: Filter CC details from a file.
  - Example: Reply to a .txt file containing CC details with `/fcc` to extract valid CC data.
- **/extp [File or BIN]**: Extrapolate credit card data from a BIN.
  - Example: `/extp 460827` (Generates extrapolated CC using BIN 460827)
- **/mgen [BINs] [Amount]**: Generate CC details using multiple BINs.
  - Example: `/mgen 460827,537637 10` (Generates 10 CC details for each BIN provided)
- **/mc [Chat Link or Usernames] [Amount]**: Scrape CC details from multiple chats.
  - Example: `/mc @Group1 @Group2 200` (Scrapes 200 CC details from both chats)
- **/topbin [File]**: Find the top 20 most used BINs from a combo.
  - Example: Reply to a .txt file with `/topbin` to extract the top 20 BINs.
- **/binbank [Bank Name]**: Find BIN database by bank name.
  - Example: `/binbank Chase` (Returns BIN details for cards issued by Chase Bank)
- **/bindb [Country Name]**: Find BIN database by country name.
  - Example: `/bindb USA` (Returns BIN details for cards issued in the USA)
- **/adbin [BIN]**: Filter specific BIN cards from a combo.
  - Example: `/adbin 460827` (Filters CC details with BIN 460827 from a file or message)
- **/rmbin [BIN]**: Remove specific BIN cards from a combo.
  - Example: `/rmbin 460827` (Removes CC details with BIN 460827 from a file or message)

### 🎵 Audio Extraction Command
Extract audio from a video:
- **/aud**: Reply to a video message to convert it into audio.

### 🎥 Social Media and Music Downloader
Download videos and tracks from popular platforms:
- **/fb [Video URL]**: Download a Facebook video.
  - Example: `/fb https://www.facebook.com/share/v/18VH1yNXoq/`
- **/pin [Video URL]**: Download a Pinterest video.
  - Example: `/pin https://pin.it/6GoDMRwmE`
- **/in [Video URL]**: Download Instagram Reels.
  - Example: `/in https://www.instagram.com/reel/C_vOYErJBm7/?igsh=YzljYTk1ODg3Zg==`
- **/sp [Track URL]**: Download a Spotify track.
  - Example: `/sp https://open.spotify.com/track/7ouBSPZKQpm7zQz2leJXta`
- **/yt [Video URL]**: Download a YouTube video.
  - Example: `/yt https://youtu.be/In8bfGnXavw`
- **/song [Video URL]**: Download a YouTube video as an MP3 file.
  - Example: `/song https://youtu.be/In8bfGnXavw`

### 📚 Language Tools Commands
Enhance your language skills:
- **/spell [Word]**: Correct the spelling of a word.
  - Example: `/spell teh` (Returns the corrected spelling: 'the')
- **/gra [Sentence]**: Fix grammatical issues in a sentence.
  - Example: `/gra I has a book` (Returns the corrected sentence: 'I have a book')
- **/syn [Word]**: Check synonyms and antonyms for a given word.
  - Example: `/syn happy` (Returns synonyms like 'joyful' and antonyms like 'sad')
- **/prn [Word]**: Check the pronunciation of a word.
  - Example: `/prn epitome` (Returns the pronunciation in phonetic format or audio: 'eh-pit-uh-mee')

### ℹ️ Info Command
Retrieve detailed information about any user, group, or channel:
- **/info [target]**: Example: `/info @abirxdhackz` or `/info 7303810912`

### 📋 Email and Credential Commands
Extract and scrape emails or email-password pairs:
- **/fmail**: Filter or extract emails by replying to a message or a text file.
  - Example: Reply to a message containing text or a .txt file and use `/fmail` to extract all emails.
- **/fpass**: Filter or extract email-password pairs by replying to a message or a text file.
  - Example: Reply to a message containing credentials or a .txt file and use `/fpass` to extract all email-password pairs.
- **/scrmail [Chat Username/Link] [Amount]**: Scrape email-password pairs from a Telegram group or channel.
  - Example: `/scrmail @abir_x_official 100` (Scrapes the first 100 messages from the specified group or channel for email-password pairs)

### 🏠 Random Address Generator
Generate random fake addresses:
- **/fake [Country Code or Country Name]**: Generate a random address for the specified country.
  - Example: `/fake BD` or `/fake Bangladesh`
- **/rnd [Country Code or Country Name]**: Alternative command for generating a random address.

### 💳 Stripe Key Commands
Verify and retrieve information about Stripe keys:
- **/sk [Stripe Key]**: Check whether the provided Stripe key is live or dead.
  - Example: `/sk sk_live_4eC39HqLyjWDarjtT1zdp7dc`
- **/skinfo [Stripe Key]**: Retrieve detailed information about the provided Stripe key.
  - Example: `/skinfo sk_live_4eC39HqLyjWDarjtT1zdp7dc`

### 🕒 Time Command
Get the current time and date for any country:
- **/time [Country Code]**: Fetch the current time and date of the specified country.
  - Example: `/time US` or `/time BD`

### 📧 Temporary Mail Tools
Generate and manage temporary emails:
- **/tmail**: Generate a random temporary email with a password.
  - Example: `/tmail`
- **/tmail [username]:[password]**: Generate a specific temporary email with your chosen username and password.
  - Example: `/tmail user123:securePass`
- **/cmail [mail token]**: Check the most recent 10 emails received by your temporary mail.
  - Example: `/cmail abc123token`

### 🌐 Network Tool Commands
Gather IP-related information and check HTTP/HTTPS proxies:
- **/ip [IP Address]**: Get detailed information about a specific IP address.
  - Example: `/ip 8.8.8.8`
- **/px [Proxy/Proxies]**: Check the validity and status of HTTP/HTTPS proxies.
  - Single Proxy Example: `/px 192.168.0.1:8080`
  - With Authentication: `/px 192.168.0.1:8080 user password`
  - Multiple Proxies Example: `/px 192.168.0.1:8080 10.0.0.2:3128 172.16.0.3:8080 user password`

### 🔑 Telegram String Session Generator
Generate string sessions for managing Telegram accounts programmatically:
- **/pyro**: Generate a Pyrogram Telegram string session.
  - Example: `/pyro`
- **/tele**: Generate a Telethon Telegram string session.
  - Example: `/tele`

### 🎨 Sticker Commands
Create or customize stickers:
- **/q**: Generate a sticker from any text message.
  - Example: Reply to any text message in the chat with `/q` to convert it into a sticker.
- **/kang**: Add any image, sticker, or animated sticker to your personal sticker pack.
  - Example: Reply to an image, sticker, or animated sticker with `/kang` to add it to your pack.

### 🌐 Translation Commands
Translate text into various languages:
- **/tr [Language Code] [Text]**: Translate the given text into the specified language.
  - Example: `/tr es Hello!` (Translates 'Hello!' to Spanish)
  - Reply Example: Reply to any message with `/tres` to translate it into Spanish.
- **/tr en [Text]**: Translate the given text into English.
  - Example: `/tr en Hola!` (Translates 'Hola!' to English)
  - Reply Example: Reply to any message with `/tr en` to translate it into English.
- **/tr bn [Text]**: Translate the given text into Bengali.
  - Example: `/tr bn Hello!` (Translates 'Hello!' to Bengali)
  - Reply Example: Reply to any message with `/tr bn` to translate it into Bengali.

### 🔍 OCR Command
Extract English text from an image:
- **/ocr**: Reply to an image to extract readable English text from it.

### 🌐 Web Tools Commands
Perform webpage-related tasks like taking screenshots or downloading source code:
- **/ss [Website URL]**: Take a screenshot of the specified webpage.
  - Example: `/ss https://example.com`
- **/ws [Website URL]**: Download the HTML source code of the specified webpage.
  - Example: `/ws https://example.com`

### 🎥 YouTube Tools Commands
Extract tags or download thumbnails from YouTube videos:
- **/ytag [YouTube Video URL]**: Extract all tags from a YouTube video.
  - Example: `/ytag https://youtu.be/In8bfGnXavw`
- **/yth [YouTube Video URL]**: Download the thumbnail of a YouTube video.
  - Example: `/yth https://youtu.be/In8bfGnXavw`

## About

- **Name**: Smart Tool ⚙️
- **Version**: 3.0 (Beta Testing) 🛠
- **Creator**: [⏤͟͞〲ᗩᗷiᖇ 𓊈乂ᗪ𓊉 👨‍💻](https://t.me/abirxdhackz)
- **Technical Stack**:
  - **Language**: Python 🐍
  - **Libraries**: Aiogram, Pyrogram, and Telethon 📚
  - **Database**: MongoDB Database 🗄
  - **Hosting**: Hostinger VPS 🌐
- **Description**: Smart Tool ⚙️ is more than just a toolkit; it’s a gateway to a world of possibilities, designed to make your everyday life simpler, smarter, and more efficient—all within the convenience of Telegram. Imagine having a treasure trove of tools and features right at your fingertips, ready to tackle challenges with precision and ease. Whether you’re an innovator, a student, a professional, or just someone looking to save time and effort, Smart Tool is here to transform the way you work, learn, and create.

For the latest updates, join our [Telegram Channel](https://t.me/ModVipRM).

## Deploy to VPS

1. **Clone the repository:**
   ```sh
   git clone https://github.com/xdmethodz/SmartTool
   cd SmartTool
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the bot:**
   ```sh
   screen -S SmartTool
   python3 main.py
   ```

## Note

This bot is still under development by [@abirxdhackz](https://t.me/abirxdhackz) and will have more updates in the future. Please do not copy the repository; only forking is allowed.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Thank you for using Smart Tool ⚙️! If you have any questions or feedback, feel free to reach out to us on our Telegram channel.

## Important Note

The tools provided by this bot are intended strictly for programming and educational purposes. They are not intended to violate any laws or regulations.
