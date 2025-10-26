import os
import yt_dlp
from config import Config

class VideoDownloader:
    def __init__(self):
        self.download_dir = Config.DOWNLOAD_DIR
        os.makedirs(self.download_dir, exist_ok=True)
    
    def download_youtube_video(self, url, output_filename=None):
        """Download a YouTube video using yt-dlp"""
        try:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
            }
            
            if output_filename:
                ydl_opts['outtmpl'] = os.path.join(self.download_dir, output_filename)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                print(f"✓ Downloaded: {info.get('title', 'Unknown')}")
                print(f"  Duration: {info.get('duration', 0)} seconds")
                print(f"  File: {filename}")
                
                return {
                    'filepath': filename,
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'description': info.get('description', ''),
                    'uploader': info.get('uploader', ''),
                }
        except Exception as e:
            print(f"✗ Error downloading video: {str(e)}")
            return None
    
    def download_from_url(self, url):
        """Download video from any supported URL"""
        if 'youtube.com' in url or 'youtu.be' in url:
            return self.download_youtube_video(url)
        else:
            # Generic download for other platforms
            return self.download_youtube_video(url)
    
    def get_video_info(self, url):
        """Get video information without downloading"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'description': info.get('description', ''),
                    'uploader': info.get('uploader', ''),
                    'view_count': info.get('view_count', 0),
                }
        except Exception as e:
            print(f"✗ Error getting video info: {str(e)}")
            return None
