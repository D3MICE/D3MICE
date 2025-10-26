#!/usr/bin/env python3
"""
AI Video Clipper Agent
Automatically clips YouTube videos and posts to social media
"""

import os
import sys
import argparse
from config import Config
from video_downloader import VideoDownloader
from clip_detector import ClipDetector
from video_processor import VideoProcessor
from social_uploader import SocialUploader

class VideoClipperAgent:
    def __init__(self):
        self.downloader = VideoDownloader()
        self.detector = ClipDetector()
        self.processor = VideoProcessor()
        self.uploader = SocialUploader()
        
        # Create necessary directories
        for directory in [Config.DOWNLOAD_DIR, Config.CLIPS_DIR, Config.TEMP_DIR]:
            os.makedirs(directory, exist_ok=True)
    
    def process_video(self, video_url, auto_upload=False, num_clips=3):
        """Main workflow to process a video"""
        print("\n" + "="*60)
        print("AI VIDEO CLIPPER AGENT")
        print("="*60 + "\n")
        
        # Step 1: Download video
        print("Step 1: Downloading video...")
        video_info = self.downloader.download_from_url(video_url)
        
        if not video_info:
            print("✗ Failed to download video")
            return False
        
        video_path = video_info['filepath']
        print(f"✓ Video downloaded: {video_path}\n")
        
        # Step 2: Detect clips
        print("Step 2: Analyzing video and detecting clips...")
        clips = self.detector.find_best_clips(video_path, video_info)
        
        if not clips:
            print("✗ No suitable clips found")
            return False
        
        print(f"✓ Found {len(clips)} clips\n")
        
        # Step 3: Extract clips
        print("Step 3: Extracting clips...")
        extracted_clips = []
        
        for i, clip in enumerate(clips[:num_clips]):
            print(f"\nClip {i+1}/{min(num_clips, len(clips))}:")
            print(f"  Time: {clip['start']:.1f}s - {clip['end']:.1f}s ({clip['duration']:.1f}s)")
            print(f"  Reason: {clip.get('reason', 'N/A')}")
            
            output_name = f"clip_{i+1}_{video_info['title'][:30].replace(' ', '_')}.mp4"
            output_path = self.processor.extract_clip(
                video_path,
                clip['start'],
                clip['end'],
                output_name
            )
            
            if output_path:
                extracted_clips.append({
                    'path': output_path,
                    'info': clip,
                    'metadata': self.uploader.generate_metadata(video_info['title'], clip)
                })
        
        print(f"\n✓ Extracted {len(extracted_clips)} clips\n")
        
        # Step 4: Upload to social media
        if auto_upload and extracted_clips:
            print("Step 4: Uploading to social media...")
            
            for i, clip_data in enumerate(extracted_clips):
                print(f"\nUploading clip {i+1}/{len(extracted_clips)}...")
                results = self.uploader.upload_to_platforms(
                    clip_data['path'],
                    clip_data['metadata']
                )
                
                for result in results:
                    if result.get('status') == 'success':
                        print(f"  ✓ {result['platform']}: {result.get('url', 'Uploaded')}")
                    else:
                        print(f"  ✗ {result['platform']}: {result.get('message', result.get('error', 'Failed'))}")
        else:
            print("Step 4: Skipping upload (use --upload flag to enable)")
            print(f"\nClips saved in: {Config.CLIPS_DIR}/")
            for clip_data in extracted_clips:
                print(f"  - {os.path.basename(clip_data['path'])}")
        
        print("\n" + "="*60)
        print("✓ PROCESSING COMPLETE")
        print("="*60 + "\n")
        
        return True
    
    def list_clips(self):
        """List all generated clips"""
        clips_dir = Config.CLIPS_DIR
        if not os.path.exists(clips_dir):
            print("No clips directory found")
            return
        
        clips = [f for f in os.listdir(clips_dir) if f.endswith('.mp4')]
        
        if not clips:
            print("No clips found")
            return
        
        print(f"\nFound {len(clips)} clips in {clips_dir}:")
        for clip in clips:
            size = os.path.getsize(os.path.join(clips_dir, clip)) / (1024 * 1024)
            print(f"  - {clip} ({size:.1f} MB)")
    
    def clean_downloads(self):
        """Clean up downloaded videos"""
        import shutil
        for directory in [Config.DOWNLOAD_DIR, Config.TEMP_DIR]:
            if os.path.exists(directory):
                shutil.rmtree(directory)
                os.makedirs(directory)
        print("✓ Cleaned up downloads and temp files")

def main():
    parser = argparse.ArgumentParser(
        description='AI Video Clipper Agent - Automatically clip and post videos to social media'
    )
    
    parser.add_argument(
        'url',
        nargs='?',
        help='YouTube or video URL to process'
    )
    
    parser.add_argument(
        '--upload',
        action='store_true',
        help='Automatically upload clips to social media'
    )
    
    parser.add_argument(
        '--clips',
        type=int,
        default=3,
        help='Number of clips to generate (default: 3)'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all generated clips'
    )
    
    parser.add_argument(
        '--clean',
        action='store_true',
        help='Clean up downloaded videos'
    )
    
    args = parser.parse_args()
    
    # Validate configuration
    Config.validate()
    
    agent = VideoClipperAgent()
    
    if args.list:
        agent.list_clips()
        return
    
    if args.clean:
        agent.clean_downloads()
        return
    
    if not args.url:
        parser.print_help()
        print("\nExample usage:")
        print("  python main.py 'https://www.youtube.com/watch?v=VIDEO_ID'")
        print("  python main.py 'https://www.youtube.com/watch?v=VIDEO_ID' --upload")
        print("  python main.py 'https://www.youtube.com/watch?v=VIDEO_ID' --clips 5")
        return
    
    try:
        agent.process_video(args.url, auto_upload=args.upload, num_clips=args.clips)
    except KeyboardInterrupt:
        print("\n\n✗ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
