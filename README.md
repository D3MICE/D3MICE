# AI Video Clipper Agent 🎬

An intelligent AI agent that automatically downloads YouTube videos, detects interesting moments, creates short clips, and posts them to social media platforms (YouTube Shorts, TikTok, Instagram Reels).

## Features

- 🎥 **Video Download**: Download videos from YouTube and other platforms
- 🤖 **AI-Powered Detection**: Use OpenAI GPT-4 to identify the most engaging moments
- ✂️ **Smart Clipping**: Automatically extract clips with optimal duration (15-60 seconds)
- 📱 **Vertical Format**: Convert clips to 9:16 format for social media
- 🎬 **Scene Detection**: Fallback to scene-based detection when AI is unavailable
- 📤 **Multi-Platform Upload**: Upload to YouTube Shorts, TikTok, and Instagram
- 🎨 **Video Processing**: Add captions, intros, outros, and optimize for each platform

## Installation

### Prerequisites

- Python 3.8 or higher
- FFmpeg installed on your system

### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:

```env
# OpenAI API Key (for AI-powered clip detection)
OPENAI_API_KEY=your_openai_api_key_here

# YouTube Data API v3 credentials (for uploading)
YOUTUBE_CLIENT_ID=your_youtube_client_id
YOUTUBE_CLIENT_SECRET=your_youtube_client_secret

# Clip settings
MIN_CLIP_DURATION=15
MAX_CLIP_DURATION=60
TARGET_PLATFORMS=youtube,tiktok,instagram
```

### Getting API Keys

#### OpenAI API Key
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key

#### YouTube API Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials
5. Download `credentials.json` and place it in the project root

## Usage

### Basic Usage

Process a video and generate clips (saved locally):
```bash
python main.py 'https://www.youtube.com/watch?v=VIDEO_ID'
```

### Generate More Clips

Generate 5 clips instead of the default 3:
```bash
python main.py 'https://www.youtube.com/watch?v=VIDEO_ID' --clips 5
```

### Auto-Upload to Social Media

Process and automatically upload to configured platforms:
```bash
python main.py 'https://www.youtube.com/watch?v=VIDEO_ID' --upload
```

### List Generated Clips

```bash
python main.py --list
```

### Clean Up Downloads

```bash
python main.py --clean
```

## How It Works

1. **Download**: Downloads the video using yt-dlp
2. **Analyze**: Uses AI (GPT-4) or scene detection to find interesting moments
3. **Extract**: Creates clips with optimal duration and vertical format
4. **Process**: Converts to 9:16 format, optimizes quality
5. **Upload**: Posts to configured social media platforms

## Project Structure

```
.
├── main.py                 # Main entry point
├── config.py              # Configuration management
├── video_downloader.py    # Video download functionality
├── clip_detector.py       # AI-powered clip detection
├── video_processor.py     # Video processing and formatting
├── social_uploader.py     # Social media upload handlers
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
└── README.md             # This file

Generated directories:
├── downloads/            # Downloaded videos
├── clips/               # Generated clips
└── temp/                # Temporary files
```

## Supported Platforms

### YouTube Shorts ✅
- Full API integration
- Automatic upload with metadata
- Supports public/private/unlisted

### TikTok ⚠️
- API integration requires approval
- Manual upload recommended

### Instagram Reels ⚠️
- Requires Business Account
- API integration in progress

## Advanced Features

### AI-Powered Detection

When OpenAI API key is configured, the agent uses GPT-4 to:
- Analyze video content and description
- Identify engaging moments
- Suggest optimal clip timestamps
- Generate compelling titles and descriptions

### Scene Detection Fallback

Without AI, the agent uses:
- Computer vision scene detection
- Duration-based filtering
- Quality scoring
- Smart scene merging

## Troubleshooting

### FFmpeg not found
```bash
# Install FFmpeg first
sudo apt install ffmpeg  # Ubuntu/Debian
brew install ffmpeg      # macOS
```

### YouTube download fails
- Check if the video is available in your region
- Ensure yt-dlp is up to date: `pip install -U yt-dlp`

### Upload fails
- Verify API credentials are correct
- Check if OAuth token needs refresh
- Ensure video meets platform requirements

## Examples

### Example 1: Quick Test
```bash
# Download and create 3 clips (no upload)
python main.py 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
```

### Example 2: Full Workflow
```bash
# Download, create 5 clips, and upload to all platforms
python main.py 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' --clips 5 --upload
```

### Example 3: Batch Processing
```bash
# Process multiple videos
for url in $(cat video_urls.txt); do
    python main.py "$url" --clips 3
done
```

## Performance Tips

- Use AI detection for best results (requires OpenAI API key)
- Start with 3 clips per video to save processing time
- Clean up downloads regularly to save disk space
- Use SSD storage for faster video processing

## License

MIT License - Feel free to use and modify

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions:
- Open an issue on GitHub
- Email: bishnoidaksh2900@gmail.com

## Roadmap

- [ ] Add support for more video platforms (Vimeo, Dailymotion)
- [ ] Implement automatic caption generation
- [ ] Add thumbnail generation
- [ ] Support for batch processing
- [ ] Web interface
- [ ] Docker container
- [ ] Cloud deployment options

---

Made with ❤️ by @D3MICE
