import os
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor
import re
from urllib.parse import unquote
import json
import time
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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Referer': 'https://www.pinterest.com/',
    }
    MAX_WORKERS = 100
    MAX_CONCURRENT_DOWNLOADS = 10
    DOWNLOAD_TIMEOUT = 60
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # Delay in seconds between retries

    # Ensure the TEMP_DIR exists
    TEMP_DIR.mkdir(exist_ok=True)

class ProgressTracker:
    def __init__(self, message: Message, file_size: int):
        self.message = message
        self.file_size = file_size
        self.start_time = time.time()
        self.last_update_time = 0
        self.last_edited_msg = None
        
    async def update_progress(self, current: int, _):
        now = time.time()
        if now - self.last_update_time < 2:  # Update every 2 seconds
            return
            
        self.last_update_time = now
        
        percentage = current * 100 / self.file_size
        elapsed_time = now - self.start_time
        speed = current / elapsed_time if elapsed_time > 0 else 0
        
        # Calculate progress bar (20 segments)
        filled_length = int(percentage / 100 * 20)
        progress_bar = '▓' * filled_length + '░' * (20 - filled_length)
        
        status_text = (
            f"📥 Upload Progress 📥 {progress_bar}\n"
            f"🚧 PC: {percentage:.2f}%\n"
            f"⚡️ Speed: {speed/1024/1024:.2f} MB/s\n"
            f"📶 Status: {current/1024/1024:.1f} MB of {self.file_size/1024/1024:.2f} MB"
        )
        
        try:
            if self.last_edited_msg:
                await self.last_edited_msg.edit_text(status_text)
            else:
                self.last_edited_msg = await self.message.reply_text(status_text)
        except Exception as e:
            logger.error(f"Error updating progress: {e}")

@dataclass
class PinterestMedia:
    url: str
    media_type: str
    width: int = 0
    height: int = 0
    fallback_urls: list = None

    def __post_init__(self):
        if self.fallback_urls is None:
            self.fallback_urls = []

class AsyncPool:
    def __init__(self, max_workers):
        self.semaphore = asyncio.Semaphore(max_workers)
        self.tasks = set()

    async def spawn(self, coro):
        async with self.semaphore:
            task = asyncio.create_task(coro)
            self.tasks.add(task)
            try:
                return await task
            finally:
                self.tasks.remove(task)

class PinterestDownloader:
    def __init__(self):
        self.session = None
        self.pin_patterns = [r'/pin/(\d+)', r'pin/(\d+)', r'pin_id=(\d+)']
        self.download_pool = AsyncPool(Config.MAX_CONCURRENT_DOWNLOADS)
        self.file_pool = ThreadPoolExecutor(max_workers=Config.MAX_WORKERS)
        
    async def init_session(self):
        if not self.session:
            timeout = aiohttp.ClientTimeout(total=Config.DOWNLOAD_TIMEOUT)
            self.session = aiohttp.ClientSession(headers=Config.HEADERS, timeout=timeout)

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None
        self.file_pool.shutdown(wait=True)

    async def extract_pin_id(self, url: str) -> Optional[str]:
        """Extract Pinterest pin ID from URL with retry logic"""
        await self.init_session()
        
        for attempt in range(Config.MAX_RETRIES):
            try:
                if 'pin.it' in url:
                    async with self.session.head(url, allow_redirects=True) as response:
                        url = str(response.url)
                
                for pattern in self.pin_patterns:
                    if match := re.search(pattern, url):
                        return match.group(1)
                return None
            except Exception as e:
                if attempt == Config.MAX_RETRIES - 1:
                    logger.error(f"Failed to extract pin ID after {Config.MAX_RETRIES} attempts: {e}")
                    raise
                await asyncio.sleep(Config.RETRY_DELAY)

    async def download_file(self, url: str, file_path: Path) -> bool:
        """Download file with retry logic"""
        for attempt in range(Config.MAX_RETRIES):
            try:
                async with self.session.get(url) as response:
                    if response.status == 200:
                        # Ensure the directory exists
                        file_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        # Use ThreadPoolExecutor for file I/O
                        content = await response.read()
                        await asyncio.get_event_loop().run_in_executor(
                            self.file_pool,
                            self._write_file,
                            file_path,
                            content
                        )
                        return True
            except Exception as e:
                if attempt == Config.MAX_RETRIES - 1:
                    logger.error(f"Failed to download file after {Config.MAX_RETRIES} attempts: {e}")
                    return False
                await asyncio.sleep(Config.RETRY_DELAY)
        return False
    
    @staticmethod
    def _write_file(file_path: Path, content: bytes):
        """Write file to disk (runs in thread pool)"""
        with open(file_path, 'wb') as f:
            f.write(content)

    @staticmethod
    def _cleanup_file(file_path: Path):
        """Cleanup file from disk"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            logger.error(f"Cleanup error: {e}")

    def get_highest_quality_image(self, image_url: str) -> str:
        """Convert image URL to highest quality version"""
        url = re.sub(r'/\d+x/|/\d+x\d+/', '/originals/', image_url)
        url = re.sub(r'\?.+$', '', url)
        return url

    async def get_pin_data(self, pin_id: str) -> Optional[PinterestMedia]:
        """Get pin data using webpage method"""
        for attempt in range(Config.MAX_RETRIES):
            try:
                return await self.get_data_from_webpage(pin_id)
            except Exception as e:
                if attempt == Config.MAX_RETRIES - 1:
                    logger.error(f"Error getting pin data after {Config.MAX_RETRIES} attempts: {e}")
                    return None
                await asyncio.sleep(Config.RETRY_DELAY)

    async def get_data_from_api(self, pin_id: str) -> Optional[PinterestMedia]:
        """Get highest quality image data from Pinterest's API"""
        api_url = f"https://api.pinterest.com/v3/pidgets/pins/info/?pin_ids={pin_id}"
        
        async with self.session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()
                if pin_data := data.get('data', [{}])[0].get('pin'):
                    if videos := pin_data.get('videos', {}).get('video_list', {}):
                        video_formats = list(videos.values())
                        if video_formats:
                            best_video = max(video_formats, key=lambda x: x.get('width', 0) * x.get('height', 0))
                            return PinterestMedia(
                                url=best_video.get('url'),
                                media_type='video',
                                width=best_video.get('width', 0),
                                height=best_video.get('height', 0)
                            )
                    
                    if images := pin_data.get('images', {}):
                        if orig_image := images.get('orig'):
                            image_url = self.get_highest_quality_image(orig_image.get('url'))
                            return PinterestMedia(
                                url=image_url,
                                media_type='image',
                                width=orig_image.get('width', 0),
                                height=orig_image.get('height', 0)
                            )
        return None

    async def get_data_from_webpage(self, pin_id: str) -> Optional[PinterestMedia]:
        """Get media data from webpage with enhanced parsing"""
        url = f"https://www.pinterest.com/pin/{pin_id}/"
        
        async with self.session.get(url) as response:
            if response.status == 200:
                text = await response.text()
                
                video_matches = re.findall(r'"url":"([^"]*?\.mp4[^"]*)"', text)
                if video_matches:
                    video_url = unquote(video_matches[0].replace('\\/', '/'))
                    return PinterestMedia(
                        url=video_url,
                        media_type='video'
                    )

                image_patterns = [
                    r'<meta property="og:image" content="([^"]+)"',
                    r'"originImageUrl":"([^"]+)"',
                    r'"image_url":"([^"]+)"',
                ]
                
                for pattern in image_patterns:
                    if matches := re.findall(pattern, text):
                        for match in matches:
                            image_url = unquote(match.replace('\\/', '/'))
                            if any(ext in image_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                                return PinterestMedia(
                                    url=self.get_highest_quality_image(image_url),
                                    media_type='image'
                                )
                
                json_pattern = r'<script[^>]*?>\s*?({.+?})\s*?</script>'
                for json_match in re.finditer(json_pattern, text):
                    try:
                        data = json.loads(json_match.group(1))
                        if isinstance(data, dict):
                            def find_image_url(d):
                                if isinstance(d, dict):
                                    for k, v in d.items():
                                        if isinstance(v, str) and any(ext in v.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                                            return v
                                        elif isinstance(v, (dict, list)):
                                            result = find_image_url(v)
                                            if result:
                                                return result
                                elif isinstance(d, list):
                                    for item in d:
                                        result = find_image_url(item)
                                        if result:
                                            return result
                                return None

                            if image_url := find_image_url(data):
                                return PinterestMedia(
                                    url=self.get_highest_quality_image(image_url),
                                    media_type='image'
                                )
                    except json.JSONDecodeError:
                        continue

        return None

    async def get_data_from_mobile_api(self, pin_id: str) -> Optional[PinterestMedia]:
        """Get highest quality media from mobile API"""
        mobile_api_url = f"https://www.pinterest.com/_ngapi/pins/{pin_id}"
        
        headers = {**Config.HEADERS, 'Accept': 'application/json'}
        async with self.session.get(mobile_api_url, headers=headers) as response:
            if response.status == 200:
                try:
                    data = await response.json()
                    
                    if video_data := data.get('videos', {}).get('video_list', {}):
                        best_video = max(
                            video_data.values(),
                            key=lambda x: x.get('width', 0) * x.get('height', 0)
                        )
                        if 'url' in best_video:
                            return PinterestMedia(
                                url=best_video['url'],
                                media_type='video',
                                width=best_video.get('width', 0),
                                height=best_video.get('height', 0)
                            )
                    
                    if image_data := data.get('images', {}):
                        if orig_image := image_data.get('orig'):
                            image_url = self.get_highest_quality_image(orig_image.get('url'))
                            return PinterestMedia(
                                url=image_url,
                                media_type='image',
                                width=orig_image.get('width', 0),
                                height=orig_image.get('height', 0)
                            )
                except json.JSONDecodeError:
                    pass
        
        return None

async def handle_pinterest_request(client, message, url):
    async with client.download_semaphore:
        try:
            # Send initial processing message
            status_msg = await message.reply_text("`Processing your request...`", parse_mode=ParseMode.MARKDOWN)
            
            # Ensure the downloader is an instance of PinterestDownloader
            if not hasattr(client, 'downloader') or not isinstance(client.downloader, PinterestDownloader):
                client.downloader = PinterestDownloader()
            
            pin_id = await client.downloader.extract_pin_id(url)
            if not pin_id:
                await status_msg.edit_text('Invalid Pinterest URL. Please send a valid pin URL.')
                return
            
            media_data = await client.downloader.get_pin_data(pin_id)
            
            if not media_data:
                await status_msg.edit_text('Could not find media in this Pinterest link.')
                return
            
            file_path = Config.TEMP_DIR / f"temp_{message.chat.id}_{message.id}_{pin_id}"
            file_path = file_path.with_suffix('.mp4' if media_data.media_type == 'video' else '.jpg')
            
            success = await client.downloader.download_pool.spawn(
                client.downloader.download_file(media_data.url, file_path)
            )
            
            if not success:
                await status_msg.edit_text('Failed to download media. Please try again later.')
                return
            
            await status_msg.delete()
            downloading_message = await message.reply_text("`Found ☑️ Downloading...`", parse_mode=ParseMode.MARKDOWN)
            
            # Get file size for progress tracking
            file_size = os.path.getsize(file_path)
            progress = ProgressTracker(message, file_size)
            
            try:
                if media_data.media_type == "video":
                    await message.reply_video(
                        video=str(file_path),
                        progress=progress.update_progress
                    )
                else:
                    await message.reply_photo(
                        photo=str(file_path),
                        progress=progress.update_progress
                    )
                
                # Clean up status messages
                await downloading_message.delete()
                if progress.last_edited_msg:
                    await progress.last_edited_msg.delete()
                    
            except Exception as e:
                logger.error(f"Error sending media: {e}")
                await status_msg.edit_text('Failed to send media. Please try again later.')
            
            await asyncio.get_event_loop().run_in_executor(
                client.downloader.file_pool,
                client.downloader._cleanup_file,
                file_path
            )
            
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            await message.reply_text('An error occurred while processing your request.')

def setup_pinterest_handler(app: Client):
    @app.on_message(filters.regex(r"^[/.](pin|pnt)(\s+\S+)?$") & (filters.private | filters.group))
    async def pin_command(client, message):
        command_parts = message.text.split(maxsplit=1)
        url = command_parts[1] if len(command_parts) > 1 else None
        if not url:
            await message.reply_text("**Please provide a Pinterest video link ❌**", parse_mode=ParseMode.MARKDOWN)
        else:
            await handle_pinterest_request(client, message, url)

    # Link the downloader and semaphore to the app for access in handlers
    app.downloader = PinterestDownloader()
    app.download_semaphore = asyncio.Semaphore(Config.MAX_CONCURRENT_DOWNLOADS)
