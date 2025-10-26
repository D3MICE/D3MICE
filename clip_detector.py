import os
import json
from moviepy.editor import VideoFileClip
from scenedetect import detect, ContentDetector, AdaptiveDetector
from config import Config

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI not available. Using basic scene detection only.")

class ClipDetector:
    def __init__(self):
        self.min_duration = Config.MIN_CLIP_DURATION
        self.max_duration = Config.MAX_CLIP_DURATION
        self.openai_client = None
        
        if OPENAI_AVAILABLE and Config.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
    
    def detect_scenes(self, video_path):
        """Detect scene changes in the video"""
        try:
            print(f"Detecting scenes in: {video_path}")
            scene_list = detect(video_path, ContentDetector(threshold=27.0))
            
            scenes = []
            for i, scene in enumerate(scene_list):
                start_time = scene[0].get_seconds()
                end_time = scene[1].get_seconds()
                duration = end_time - start_time
                
                scenes.append({
                    'scene_id': i,
                    'start': start_time,
                    'end': end_time,
                    'duration': duration
                })
            
            print(f"✓ Detected {len(scenes)} scenes")
            return scenes
        except Exception as e:
            print(f"✗ Error detecting scenes: {str(e)}")
            return []
    
    def analyze_video_with_ai(self, video_path, video_info):
        """Use AI to identify interesting moments for clips"""
        if not self.openai_client:
            print("AI analysis not available. Using scene-based detection.")
            return None
        
        try:
            prompt = f"""
            Analyze this video and suggest the best moments to create short clips (15-60 seconds).
            
            Video Title: {video_info.get('title', 'Unknown')}
            Duration: {video_info.get('duration', 0)} seconds
            Description: {video_info.get('description', '')[:500]}
            
            Suggest 3-5 clip timestamps that would be:
            1. Engaging and attention-grabbing
            2. Self-contained (make sense without context)
            3. Suitable for social media (TikTok, YouTube Shorts, Instagram Reels)
            
            Return as JSON array with format:
            [
                {{"start": 10, "end": 45, "reason": "Exciting moment with high energy"}},
                ...
            ]
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a video editing expert specializing in creating viral short-form content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            suggestions = json.loads(response.choices[0].message.content)
            print(f"✓ AI suggested {len(suggestions)} clips")
            return suggestions
            
        except Exception as e:
            print(f"✗ Error in AI analysis: {str(e)}")
            return None
    
    def find_best_clips(self, video_path, video_info):
        """Find the best clips from the video"""
        clips = []
        
        # Try AI analysis first
        ai_suggestions = self.analyze_video_with_ai(video_path, video_info)
        
        if ai_suggestions:
            for i, suggestion in enumerate(ai_suggestions):
                clips.append({
                    'clip_id': i,
                    'start': suggestion['start'],
                    'end': suggestion['end'],
                    'duration': suggestion['end'] - suggestion['start'],
                    'reason': suggestion.get('reason', 'AI suggested'),
                    'method': 'ai'
                })
        else:
            # Fallback to scene detection
            scenes = self.detect_scenes(video_path)
            
            # Merge consecutive short scenes
            merged_clips = []
            current_clip = None
            
            for scene in scenes:
                if current_clip is None:
                    current_clip = scene.copy()
                elif (scene['start'] - current_clip['end'] < 2 and 
                      current_clip['duration'] + scene['duration'] <= self.max_duration):
                    current_clip['end'] = scene['end']
                    current_clip['duration'] = current_clip['end'] - current_clip['start']
                else:
                    if self.min_duration <= current_clip['duration'] <= self.max_duration:
                        merged_clips.append(current_clip)
                    current_clip = scene.copy()
            
            if current_clip and self.min_duration <= current_clip['duration'] <= self.max_duration:
                merged_clips.append(current_clip)
            
            # Take top clips by duration
            merged_clips.sort(key=lambda x: x['duration'], reverse=True)
            clips = merged_clips[:5]
            
            for i, clip in enumerate(clips):
                clip['clip_id'] = i
                clip['reason'] = 'Scene-based detection'
                clip['method'] = 'scene'
        
        print(f"✓ Found {len(clips)} potential clips")
        return clips
    
    def score_clip_quality(self, video_path, start, end):
        """Score a clip based on various quality metrics"""
        try:
            clip = VideoFileClip(video_path).subclip(start, end)
            
            # Basic quality metrics
            score = 50  # Base score
            
            # Duration score (prefer 30-45 seconds)
            duration = end - start
            if 30 <= duration <= 45:
                score += 20
            elif 20 <= duration <= 50:
                score += 10
            
            # Resolution score
            if clip.h >= 720:
                score += 15
            
            # Audio score
            if clip.audio is not None:
                score += 15
            
            clip.close()
            return score
            
        except Exception as e:
            print(f"Warning: Could not score clip: {str(e)}")
            return 50
