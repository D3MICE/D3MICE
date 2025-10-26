# Quick Start Guide 🚀

Get started with the AI Video Clipper Agent in 5 minutes!

## Prerequisites

- Python 3.8+
- FFmpeg
- OpenAI API key (optional, for AI features)
- YouTube API credentials (optional, for uploading)

## Installation

### 1. Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example config
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

Minimum configuration:
```env
OPENAI_API_KEY=your_key_here
MIN_CLIP_DURATION=15
MAX_CLIP_DURATION=60
TARGET_PLATFORMS=youtube
```

## Usage

### Run Demo (No Dependencies Required)

```bash
python3 demo.py
```

See features:
```bash
python3 demo.py --features
```

See examples:
```bash
python3 demo.py --examples
```

### Process a Video

**Basic (save clips locally):**
```bash
python main.py 'https://www.youtube.com/watch?v=VIDEO_ID'
```

**Generate 5 clips:**
```bash
python main.py 'https://www.youtube.com/watch?v=VIDEO_ID' --clips 5
```

**Auto-upload to social media:**
```bash
python main.py 'https://www.youtube.com/watch?v=VIDEO_ID' --upload
```

## What Happens?

1. **Downloads** the video from YouTube
2. **Analyzes** content using AI (GPT-4) or scene detection
3. **Extracts** 3-5 engaging clips (15-60 seconds each)
4. **Converts** to vertical format (9:16) for social media
5. **Uploads** to YouTube Shorts, TikTok, Instagram (if enabled)

## Output

Clips are saved in the `clips/` directory:
```
clips/
├── clip_1_Video_Title.mp4
├── clip_2_Video_Title.mp4
└── clip_3_Video_Title.mp4
```

## Tips

- Start without `--upload` to preview clips first
- Use AI detection for best results (requires OpenAI API key)
- Clean up downloads regularly: `python main.py --clean`
- List generated clips: `python main.py --list`

## Troubleshooting

**"No module named 'dotenv'"**
```bash
pip install python-dotenv
```

**"FFmpeg not found"**
```bash
# Install FFmpeg first (see step 1)
```

**"YouTube download failed"**
- Check if video is available in your region
- Update yt-dlp: `pip install -U yt-dlp`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Configure YouTube API for uploading
- Customize clip duration in `.env`
- Add custom captions and branding

## Support

- GitHub Issues: [Report a bug]
- Email: bishnoidaksh2900@gmail.com

---

Happy clipping! 🎬✨
