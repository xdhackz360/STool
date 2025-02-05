import os

# Replace these with your actual API details
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_STRING = os.getenv("SESSION_STRING")

# Admin IDs Replace With Actual IDS
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))

# CC Scraper Limits
DEFAULT_LIMIT = int(os.getenv("DEFAULT_LIMIT", 10000))
ADMIN_LIMIT = int(os.getenv("ADMIN_LIMIT", 50000))

# List of owner ids (add your owner ids here)
OWNERS = list(map(int, os.getenv("OWNERS", "").split(",")))

# MongoDB connection setup
MONGO_URL = os.getenv("MONGO_URL")

# Configuration for Google Generative AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")

# Spotify Configuration
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

OWNER_ID = int(os.getenv("OWNER_ID"))

# Cricbuzz Api Setup
API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")

# News API Key
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Bin Api Key
BIN_KEY = os.getenv("BIN_KEY")
