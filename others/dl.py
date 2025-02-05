import os
import logging
from pathlib import Path
from typing import Optional
import yt_dlp
import asyncio
import aiofiles
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
class Config:
    TEMP_DIR = Path("temp")
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Referer': 'https://www.pinterest.com/',
    }

Config.TEMP_DIR.mkdir(exist_ok=True)

class FacebookDownloader:
    def __init__(self, temp_dir: Path):
        self.temp_dir = temp_dir
        yt_dlp.utils.std_headers['User-Agent'] = Config.HEADERS['User-Agent']

    async def download_video(self, url: str) -> Optional[dict]:
        self.temp_dir.mkdir(exist_ok=True)
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': str(self.temp_dir / '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'no_color': True,
            'simulate': False,
            'nooverwrites': True,
        }

        try:
            loop = asyncio.get_event_loop()
            video_info = await loop.run_in_executor(None, self._download_video, ydl_opts, url)
            return video_info
        except Exception as e:
            logger.error(f"Facebook download error: {e}")
            return None

    def _download_video(self, ydl_opts, url):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            if os.path.exists(filename):
                return {
                    'title': info_dict.get('title', 'Unknown Title'),
                    'filename': filename,
                    'resolution': f"{info_dict.get('height', 'Unknown')}p",
                    'views': info_dict.get('view_count', 'Unknown'),
                    'duration': info_dict.get('duration', 'Unknown'),
                    'webpage_url': info_dict.get('webpage_url', url)
                }
            else:
                return None

def setup_dl_handlers(app: Client):
    fb_downloader = FacebookDownloader(Config.TEMP_DIR)

    @app.on_message(filters.regex(r"^[/.]fb(\s+https?://\S+)?$") & (filters.private | filters.group))
    async def fb_handler(client: Client, message: Message):
        command_parts = message.text.split(maxsplit=1)
        if len(command_parts) < 2:
            await message.reply_text("**Please provide a Facebook video URL after the command.**", parse_mode=ParseMode.MARKDOWN)
            return
        
        url = command_parts[1]
        downloading_message = await message.reply_text("`Searching The Video`", parse_mode=ParseMode.MARKDOWN)
        
        try:
            video_info = await fb_downloader.download_video(url)
            if video_info:
                await downloading_message.edit_text("`Downloading Your Video ...`", parse_mode=ParseMode.MARKDOWN)
                
                title = video_info['title']
                filename = video_info['filename']
                resolution = video_info['resolution']
                views = video_info['views']
                duration = video_info['duration']
                webpage_url = video_info['webpage_url']
                
                if message.from_user:
                    user_full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
                    user_info = f"[{user_full_name}](tg://user?id={message.from_user.id})"
                else:
                    group_name = message.chat.title or "this group"
                    group_url = f"https://t.me/{message.chat.username}" if message.chat.username else "this group"
                    user_info = f"[{group_name}]({group_url})"

                # Convert duration to minutes and seconds
                duration_minutes = int(duration // 60)
                duration_seconds = int(duration % 60)
                
                caption = (
                    f"🎵 **Title**: `{title}`\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n"
                    f"👁️‍🗨️ **Views**: `{views} views`\n"
                    f"🔗 **Url**: [Watch On Facebook]({webpage_url})\n"
                    f"⏱️ **Duration**: `{duration_minutes}:{duration_seconds:02d}`\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n"
                    f"**Downloaded By**: {user_info}"
                )
                
                await message.reply_video(video=filename, supports_streaming=True, caption=caption, parse_mode=ParseMode.MARKDOWN)
                
                await downloading_message.delete()
                os.remove(filename)
            else:
                await downloading_message.edit_text("Could not download the video.")
        except Exception as e:
            logger.error(f"Error downloading Facebook video: {e}")
            await downloading_message.edit_text("An error occurred while processing your request.")
