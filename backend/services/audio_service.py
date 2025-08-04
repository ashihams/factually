import requests
import os
from typing import Dict, Any
import json

class AudioService:
    def __init__(self):
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        self.base_url = "https://api.elevenlabs.io/v1"
        
        # Default voice settings for professional narration
        self.default_voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel - professional female voice
        self.voice_settings = {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True
        }
    
    async def generate_audio(self, text: str, voice_id: str = None) -> Dict[str, Any]:
        """
        Generate high-quality voice-over audio using ElevenLabs API
        """
        try:
            if not voice_id:
                voice_id = self.default_voice_id
            
            url = f"{self.base_url}/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": self.voice_settings
            }
            
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            # Save audio to file
            audio_filename = f"audio_{hash(text) % 10000}.mp3"
            audio_path = f"static/audio/{audio_filename}"
            
            # Ensure directory exists
            os.makedirs("static/audio", exist_ok=True)
            
            with open(audio_path, "wb") as f:
                f.write(response.content)
            
            return {
                'audio_url': f"/static/audio/{audio_filename}",
                'audio_path': audio_path,
                'duration': self._estimate_duration(text),
                'voice_id': voice_id,
                'text_length': len(text)
            }
            
        except Exception as e:
            print(f"Error generating audio: {str(e)}")
            raise e
    
    async def get_available_voices(self) -> list:
        """
        Get list of available voices
        """
        try:
            url = f"{self.base_url}/voices"
            headers = {
                "Accept": "application/json",
                "xi-api-key": self.api_key
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            return data.get('voices', [])
            
        except Exception as e:
            print(f"Error fetching voices: {str(e)}")
            return []
    
    async def generate_audio_for_script(self, script_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate audio for a complete script
        """
        try:
            narrator_text = script_data.get('narrator_text', '')
            
            if not narrator_text:
                raise Exception("No narrator text found in script")
            
            # Clean and prepare text for TTS
            clean_text = self._prepare_text_for_tts(narrator_text)
            
            # Generate audio
            audio_data = await self.generate_audio(clean_text)
            
            return {
                'script_data': script_data,
                'audio_data': audio_data,
                'status': 'success'
            }
            
        except Exception as e:
            print(f"Error generating audio for script: {str(e)}")
            raise e
    
    def _prepare_text_for_tts(self, text: str) -> str:
        """
        Prepare text for text-to-speech
        """
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove any remaining scene markers
        text = text.replace('Scene:', '').replace('scene:', '')
        
        # Ensure proper punctuation
        if not text.endswith(('.', '!', '?')):
            text += '.'
        
        return text
    
    def _estimate_duration(self, text: str) -> float:
        """
        Estimate audio duration based on text length
        Average speaking rate: 150 words per minute
        """
        word_count = len(text.split())
        duration_minutes = word_count / 150
        return round(duration_minutes * 60, 2)  # Return in seconds
    
    async def generate_multiple_audio(self, scripts: list) -> list:
        """
        Generate audio for multiple scripts
        """
        audio_results = []
        
        for script_item in scripts:
            try:
                audio_result = await self.generate_audio_for_script(script_item['script_data'])
                audio_results.append({
                    'article': script_item['article'],
                    'script_data': script_item['script_data'],
                    'audio_data': audio_result['audio_data']
                })
                
            except Exception as e:
                print(f"Error generating audio for script: {str(e)}")
                continue
        
        return audio_results 