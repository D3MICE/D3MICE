import os
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from config import Config

class SocialUploader:
    def __init__(self):
        self.youtube_service = None
        self.credentials_file = 'credentials.json'
        self.token_file = 'token.pickle'
    
    def authenticate_youtube(self):
        """Authenticate with YouTube API"""
        try:
            creds = None
            SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
            
            if os.path.exists(self.token_file):
                with open(self.token_file, 'rb') as token:
                    creds = pickle.load(token)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                elif os.path.exists(self.credentials_file):
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, SCOPES)
                    creds = flow.run_local_server(port=0)
                else:
                    print("✗ YouTube credentials file not found. Please add credentials.json")
                    return False
                
                with open(self.token_file, 'wb') as token:
                    pickle.dump(creds, token)
            
            self.youtube_service = build('youtube', 'v3', credentials=creds)
            print("✓ YouTube authentication successful")
            return True
            
        except Exception as e:
            print(f"✗ YouTube authentication failed: {str(e)}")
            return False
    
    def upload_to_youtube(self, video_path, title, description, tags=None, category='22'):
        """Upload video to YouTube as a Short"""
        if not self.youtube_service:
            if not self.authenticate_youtube():
                return None
        
        try:
            # Add #Shorts to description for YouTube Shorts
            if '#Shorts' not in description:
                description = f"{description}\n\n#Shorts"
            
            body = {
                'snippet': {
                    'title': title[:100],  # YouTube title limit
                    'description': description[:5000],  # YouTube description limit
                    'tags': tags or ['shorts', 'viral', 'trending'],
                    'categoryId': category
                },
                'status': {
                    'privacyStatus': 'public',  # or 'private', 'unlisted'
                    'selfDeclaredMadeForKids': False
                }
            }
            
            media = MediaFileUpload(
                video_path,
                chunksize=-1,
                resumable=True,
                mimetype='video/*'
            )
            
            request = self.youtube_service.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            print(f"Uploading to YouTube: {title}")
            response = request.execute()
            
            video_id = response['id']
            video_url = f"https://www.youtube.com/shorts/{video_id}"
            
            print(f"✓ Uploaded to YouTube: {video_url}")
            return {
                'platform': 'youtube',
                'video_id': video_id,
                'url': video_url,
                'status': 'success'
            }
            
        except Exception as e:
            print(f"✗ YouTube upload failed: {str(e)}")
            return {
                'platform': 'youtube',
                'status': 'failed',
                'error': str(e)
            }
    
    def upload_to_tiktok(self, video_path, title, description):
        """Upload video to TikTok (placeholder - requires TikTok API access)"""
        print("TikTok upload: API integration required")
        print(f"  Video: {video_path}")
        print(f"  Title: {title}")
        print(f"  Description: {description}")
        
        # TikTok API integration would go here
        # Note: TikTok API access requires approval and is not publicly available
        
        return {
            'platform': 'tiktok',
            'status': 'not_implemented',
            'message': 'TikTok API integration requires approval'
        }
    
    def upload_to_instagram(self, video_path, caption):
        """Upload video to Instagram Reels (placeholder - requires Instagram API)"""
        print("Instagram upload: API integration required")
        print(f"  Video: {video_path}")
        print(f"  Caption: {caption}")
        
        # Instagram Graph API integration would go here
        # Requires Facebook App and Instagram Business Account
        
        return {
            'platform': 'instagram',
            'status': 'not_implemented',
            'message': 'Instagram API integration requires Business Account'
        }
    
    def upload_to_platforms(self, video_path, metadata):
        """Upload video to multiple platforms"""
        results = []
        
        title = metadata.get('title', 'Untitled')
        description = metadata.get('description', '')
        tags = metadata.get('tags', [])
        
        for platform in Config.TARGET_PLATFORMS:
            platform = platform.strip().lower()
            
            if platform == 'youtube':
                result = self.upload_to_youtube(video_path, title, description, tags)
                results.append(result)
            elif platform == 'tiktok':
                result = self.upload_to_tiktok(video_path, title, description)
                results.append(result)
            elif platform == 'instagram':
                result = self.upload_to_instagram(video_path, description)
                results.append(result)
        
        return results
    
    def generate_metadata(self, original_title, clip_info):
        """Generate metadata for the clip"""
        title = f"{original_title} - Clip {clip_info.get('clip_id', 1)}"
        
        description = f"""
{clip_info.get('reason', 'Interesting moment from the video')}

Original video: {original_title}

#Shorts #Viral #Trending #Clips
        """.strip()
        
        tags = ['shorts', 'viral', 'trending', 'clips', 'highlights']
        
        return {
            'title': title,
            'description': description,
            'tags': tags
        }
