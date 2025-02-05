import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from pyrogram.handlers import MessageHandler
from spellchecker import SpellChecker

# Initialize the spell checker
spell = SpellChecker()

async def check_grammar(text):
    url = "https://api.languagetool.org/v2/check"
    data = {
        'text': text,
        'language': 'en-US'
    }
    response = requests.post(url, data=data)
    result = response.json()
    corrected_text = text
    for match in result['matches']:
        offset = match['offset']
        length = match['length']
        replacement = match['replacements'][0]['value'] if match['replacements'] else ''
        corrected_text = corrected_text[:offset] + replacement + corrected_text[offset + length:]
    return corrected_text

async def grammar_check(client: Client, message: Message):
    user_input = message.text.split(maxsplit=1)  # Split the message text
    if len(user_input) < 2:
        await message.reply_text("**❌ Provide some text to fix Grammar..**", parse_mode=ParseMode.MARKDOWN)
    else:
        checking_message = await message.reply_text("**⚡️Checking Grammar Please Wait...⏳**", parse_mode=ParseMode.MARKDOWN)
        corrected_text = await check_grammar(user_input[1])
        await checking_message.delete()
        await message.reply_text(f"`{corrected_text}`", parse_mode=ParseMode.MARKDOWN)

async def check_spelling(word):
    # Use Pyspellchecker to check spelling
    misspelled = spell.unknown([word])
    if misspelled:
        corrected_word = spell.correction(list(misspelled)[0])
    else:
        corrected_word = word
    return corrected_word

async def spell_check(client: Client, message: Message):
    user_input = message.text.split(maxsplit=1)  # Split the message text
    if len(user_input) < 2:
        await message.reply_text("**❌Provide some text to check spelling..**", parse_mode=ParseMode.MARKDOWN)
    else:
        checking_message = await message.reply_text("**⚡️Checking Spelling Please Wait...⏳**", parse_mode=ParseMode.MARKDOWN)
        corrected_word = await check_spelling(user_input[1])
        await checking_message.delete()
        await message.reply_text(f"`{corrected_word}`", parse_mode=ParseMode.MARKDOWN)

async def fetch_pronunciation_info(word):
    # Use FreeDictionaryAPI to fetch word information
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    
    # Check if the response is successful
    if response.status_code != 200:
        return None
    
    try:
        result = response.json()
    except ValueError:
        return None

    if not result or isinstance(result, dict):
        return None

    data = result[0]
    definition = data['meanings'][0]['definitions'][0]['definition']
    stems = [meaning['partOfSpeech'] for meaning in data['meanings']]

    # Get audio link if available
    audio_link = None
    for phonetic in data['phonetics']:
        if phonetic['audio']:
            audio_link = phonetic['audio']
            break

    pronunciation_info = {
        "word": word.capitalize(),
        "breakdown": word,  # Placeholder, FreeDictionaryAPI does not provide breakdown
        "pronunciation": "",  # Placeholder, FreeDictionaryAPI does not provide IPA pronunciation
        "stems": stems,
        "definition": definition,
        "audio_link": audio_link  # Add audio link to info
    }

    return pronunciation_info

async def pronunciation_check(client: Client, message: Message):
    user_input = message.text.split(maxsplit=1)  # Split the message text
    if len(user_input) < 2:
        await message.reply_text("**❌Provide a word to check its pronunciation.**", parse_mode=ParseMode.MARKDOWN)
    else:
        word = user_input[1]
        checking_message = await message.reply_text("**⚡️Checking Pronunciation...⏳**", parse_mode=ParseMode.MARKDOWN)

        # Fetch pronunciation information
        pronunciation_info = await fetch_pronunciation_info(word)
        
        # Handle case where pronunciation info could not be fetched
        if pronunciation_info is None:
            await checking_message.delete()
            await message.reply_text("**❌Could not fetch pronunciation information. Please try again later.**", parse_mode=ParseMode.MARKDOWN)
            return

        audio_filename = None
        if pronunciation_info['audio_link']:
            audio_filename = f"Smart Tool ⚙️ {word}.mp3"
            # Download the audio file
            response = requests.get(pronunciation_info['audio_link'])
            with open(audio_filename, 'wb') as f:
                f.write(response.content)

        caption = (f"Word: {pronunciation_info['word']}\n"
                   f"- Breakdown: {pronunciation_info['breakdown']}\n"
                   f"- Pronunciation: {pronunciation_info['pronunciation']}\n\n"
                   f"Word Stems:\n{', '.join(pronunciation_info['stems'])}\n\n"
                   f"Definition:\n{pronunciation_info['definition']}")

        # Send the audio file with caption if audio is available
        if audio_filename:
            await client.send_audio(
                chat_id=message.chat.id,
                audio=audio_filename,
                caption=caption
            )
            # Delete the temporary audio file
            os.remove(audio_filename)
        else:
            await message.reply_text(caption, parse_mode=ParseMode.MARKDOWN)

        await checking_message.delete()

def setup_eng_handler(app: Client):
    app.add_handler(
        MessageHandler(
            grammar_check,
            filters.command(["gra"], prefixes=["/", "."]) & (filters.private | filters.group)
        )
    )
    app.add_handler(
        MessageHandler(
            spell_check,
            filters.command(["spell"], prefixes=["/", "."]) & (filters.private | filters.group)
        )
    )
    app.add_handler(
        MessageHandler(
            pronunciation_check,
            filters.command(["prn"], prefixes=["/", "."]) & (filters.private | filters.group)
        )
    )
