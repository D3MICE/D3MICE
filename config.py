import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID', '')
    YOUTUBE_CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET', '')
    TIKTOK_CLIENT_KEY = os.getenv('TIKTOK_CLIENT_KEY', '')
    TIKTOK_CLIENT_SECRET = os.getenv('TIKTOK_CLIENT_SECRET', '')
    INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN', '')
    
    # Clip Settings
    MIN_CLIP_DURATION = int(os.getenv('MIN_CLIP_DURATION', 15))
    MAX_CLIP_DURATION = int(os.getenv('MAX_CLIP_DURATION', 60))
    TARGET_PLATFORMS = os.getenv('TARGET_PLATFORMS', 'youtube').split(',')
    
    # Directories
    DOWNLOAD_DIR = 'downloads'
    CLIPS_DIR = 'clips'
    TEMP_DIR = 'temp'
    
    # Video Settings
    OUTPUT_RESOLUTION = (1080, 1920)  # Vertical format for shorts
    OUTPUT_FPS = 30
    OUTPUT_BITRATE = '5000k'
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.OPENAI_API_KEY:
            print("Warning: OPENAI_API_KEY not set. AI features will be limited.")
        return True
