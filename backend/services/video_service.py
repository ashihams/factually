import requests
import os
from typing import List, Dict, Any
import random

class VideoService:
    def __init__(self):
        self.api_key = os.getenv('PEXELS_API_KEY')
        self.base_url = "https://api.pexels.com/videos"
        
    async def fetch_videos(self, prompts: List[str]) -> List[Dict[str, Any]]:
        """
        Fetch relevant videos from Pexels API based on scene prompts
        """
        try:
            videos = []
            
            for prompt in prompts:
                try:
                    video_data = await self._fetch_single_video(prompt)
                    if video_data:
                        videos.append(video_data)
                except Exception as e:
                    print(f"Error fetching video for prompt '{prompt}': {str(e)}")
                    continue
            
            return videos
            
        except Exception as e:
            print(f"Error fetching videos: {str(e)}")
            raise e
    
    async def _fetch_single_video(self, prompt: str) -> Dict[str, Any]:
        """
        Fetch a single video for a given prompt
        """
        try:
            url = f"{self.base_url}/search"
            headers = {
                "Authorization": self.api_key
            }
            params = {
                "query": prompt,
                "per_page": 1,
                "orientation": "portrait",  # For mobile-first content
                "size": "medium"  # Good quality, reasonable file size
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('videos') and len(data['videos']) > 0:
                video = data['videos'][0]
                
                # Get the best quality video file
                video_files = video.get('video_files', [])
                if video_files:
                    # Prefer HD quality, fallback to any available
                    hd_video = next((vf for vf in video_files if vf.get('width', 0) >= 1280), None)
                    selected_video = hd_video or video_files[0]
                    
                    return {
                        'id': video.get('id'),
                        'url': selected_video.get('link'),
                        'width': selected_video.get('width'),
                        'height': selected_video.get('height'),
                        'duration': video.get('duration'),
                        'prompt': prompt,
                        'thumbnail': video.get('image'),
                        'user': video.get('user', {}).get('name', 'Unknown'),
                        'description': video.get('url', '')
                    }
            
            return None
            
        except Exception as e:
            print(f"Error fetching single video: {str(e)}")
            return None
    
    async def fetch_videos_for_script(self, script_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch videos for all scenes in a script
        """
        try:
            scenes = script_data.get('scenes', [])
            
            if not scenes:
                # If no scenes found, create generic prompts from script
                script_text = script_data.get('script', '')
                scenes = self._extract_generic_prompts(script_text)
            
            videos = await self.fetch_videos(scenes)
            
            return {
                'script_data': script_data,
                'videos': videos,
                'scene_count': len(scenes),
                'video_count': len(videos)
            }
            
        except Exception as e:
            print(f"Error fetching videos for script: {str(e)}")
            raise e
    
    def _extract_generic_prompts(self, script_text: str) -> List[str]:
        """
        Extract generic video prompts from script text
        """
        # Common video prompts for news content
        generic_prompts = [
            "news broadcast",
            "city skyline",
            "people walking",
            "technology",
            "business meeting",
            "nature landscape"
        ]
        
        # Return a subset of generic prompts
        return random.sample(generic_prompts, min(3, len(generic_prompts)))
    
    async def fetch_trending_videos(self, category: str = "nature", per_page: int = 5) -> List[Dict[str, Any]]:
        """
        Fetch trending videos from Pexels
        """
        try:
            url = f"{self.base_url}/popular"
            headers = {
                "Authorization": self.api_key
            }
            params = {
                "per_page": per_page
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            videos = []
            for video in data.get('videos', []):
                video_files = video.get('video_files', [])
                if video_files:
                    selected_video = video_files[0]
                    videos.append({
                        'id': video.get('id'),
                        'url': selected_video.get('link'),
                        'width': selected_video.get('width'),
                        'height': selected_video.get('height'),
                        'duration': video.get('duration'),
                        'thumbnail': video.get('image'),
                        'user': video.get('user', {}).get('name', 'Unknown')
                    })
            
            return videos
            
        except Exception as e:
            print(f"Error fetching trending videos: {str(e)}")
            return []
    
    async def fetch_multiple_videos(self, scripts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Fetch videos for multiple scripts
        """
        video_results = []
        
        for script_item in scripts:
            try:
                video_result = await self.fetch_videos_for_script(script_item['script_data'])
                video_results.append({
                    'article': script_item['article'],
                    'script_data': script_item['script_data'],
                    'video_data': video_result
                })
                
            except Exception as e:
                print(f"Error fetching videos for script: {str(e)}")
                continue
        
        return video_results 