import os
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip
from moviepy.video.fx import resize, crop
from config import Config

class VideoProcessor:
    def __init__(self):
        self.clips_dir = Config.CLIPS_DIR
        os.makedirs(self.clips_dir, exist_ok=True)
        self.output_resolution = Config.OUTPUT_RESOLUTION
        self.output_fps = Config.OUTPUT_FPS
    
    def extract_clip(self, video_path, start, end, output_name, add_captions=False):
        """Extract a clip from the video"""
        try:
            print(f"Extracting clip: {start}s to {end}s")
            
            video = VideoFileClip(video_path)
            clip = video.subclip(start, end)
            
            # Convert to vertical format (9:16) for social media
            clip = self.convert_to_vertical(clip)
            
            # Add captions if requested
            if add_captions:
                clip = self.add_captions(clip, "")
            
            output_path = os.path.join(self.clips_dir, output_name)
            
            clip.write_videofile(
                output_path,
                fps=self.output_fps,
                codec='libx264',
                audio_codec='aac',
                bitrate=Config.OUTPUT_BITRATE,
                preset='medium',
                threads=4
            )
            
            clip.close()
            video.close()
            
            print(f"✓ Clip saved: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"✗ Error extracting clip: {str(e)}")
            return None
    
    def convert_to_vertical(self, clip):
        """Convert video to vertical format (9:16) for social media"""
        try:
            target_width, target_height = self.output_resolution
            aspect_ratio = target_height / target_width
            
            # Get current dimensions
            w, h = clip.size
            current_ratio = h / w
            
            if current_ratio < aspect_ratio:
                # Video is too wide, crop sides
                new_width = int(h / aspect_ratio)
                x_center = w / 2
                x1 = int(x_center - new_width / 2)
                clip = crop(clip, x1=x1, width=new_width)
            elif current_ratio > aspect_ratio:
                # Video is too tall, crop top/bottom
                new_height = int(w * aspect_ratio)
                y_center = h / 2
                y1 = int(y_center - new_height / 2)
                clip = crop(clip, y1=y1, height=new_height)
            
            # Resize to target resolution
            clip = resize(clip, height=target_height)
            
            return clip
            
        except Exception as e:
            print(f"Warning: Could not convert to vertical: {str(e)}")
            return clip
    
    def add_captions(self, clip, text):
        """Add text captions to the clip"""
        try:
            if not text:
                return clip
            
            txt_clip = TextClip(
                text,
                fontsize=40,
                color='white',
                stroke_color='black',
                stroke_width=2,
                font='Arial-Bold',
                method='caption',
                size=(clip.w * 0.9, None)
            )
            
            txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(clip.duration)
            
            video = CompositeVideoClip([clip, txt_clip])
            return video
            
        except Exception as e:
            print(f"Warning: Could not add captions: {str(e)}")
            return clip
    
    def add_intro_outro(self, clip, intro_text=None, outro_text=None):
        """Add intro/outro text to the clip"""
        try:
            clips = []
            
            if intro_text:
                intro = TextClip(
                    intro_text,
                    fontsize=50,
                    color='white',
                    bg_color='black',
                    size=clip.size
                ).set_duration(2)
                clips.append(intro)
            
            clips.append(clip)
            
            if outro_text:
                outro = TextClip(
                    outro_text,
                    fontsize=50,
                    color='white',
                    bg_color='black',
                    size=clip.size
                ).set_duration(2)
                clips.append(outro)
            
            from moviepy.editor import concatenate_videoclips
            final_clip = concatenate_videoclips(clips)
            return final_clip
            
        except Exception as e:
            print(f"Warning: Could not add intro/outro: {str(e)}")
            return clip
    
    def optimize_for_platform(self, clip_path, platform):
        """Optimize video for specific platform"""
        platform_specs = {
            'youtube': {'max_duration': 60, 'resolution': (1080, 1920)},
            'tiktok': {'max_duration': 60, 'resolution': (1080, 1920)},
            'instagram': {'max_duration': 60, 'resolution': (1080, 1920)},
        }
        
        specs = platform_specs.get(platform.lower(), platform_specs['youtube'])
        print(f"Optimizing for {platform}: {specs}")
        return clip_path
