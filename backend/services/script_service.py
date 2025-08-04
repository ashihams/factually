import google.generativeai as genai
import os
from typing import Dict, Any
import re

class ScriptService:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def generate_reel_script(self, news_title: str, news_content: str, news_url: str) -> Dict[str, Any]:
        """
        Generate a 1-minute reel script from news content using Gemini API
        """
        try:
            # Create a comprehensive prompt for high-quality script generation
            prompt = f"""
            Create a compelling 1-minute (150-160 words) short-form video script for a news story.
            
            News Title: {news_title}
            News Content: {news_content}
            Source: {news_url}
            
            Requirements:
            1. Create a script that's exactly 1 minute when spoken (150-160 words)
            2. Use the "Narrator:" format for voice-over sections
            3. Include "Scene:" descriptions for video background suggestions
            4. Make it engaging, informative, and suitable for social media
            5. Structure it like this:
            
            Narrator: [Opening hook - 15 seconds]
            Scene: [Visual suggestion for opening]
            
            Narrator: [Main content - 30 seconds]
            Scene: [Visual suggestion for main content]
            
            Narrator: [Key points/details - 30 seconds]
            Scene: [Visual suggestion for details]
            
            Narrator: [Closing/CTA - 15 seconds]
            Scene: [Visual suggestion for closing]
            
            Make it engaging, factual, and perfect for short-form video content.
            Focus on the most important aspects of the news story.
            """
            
            response = self.model.generate_content(prompt)
            
            if response.text:
                script = response.text.strip()
                
                # Extract scenes for video matching
                scenes = self._extract_scenes(script)
                
                # Extract narrator text for audio generation
                narrator_text = self._extract_narrator_text(script)
                
                return {
                    'script': script,
                    'scenes': scenes,
                    'narrator_text': narrator_text,
                    'word_count': len(script.split()),
                    'estimated_duration': '60 seconds'
                }
            else:
                raise Exception("No script generated")
                
        except Exception as e:
            print(f"Error generating script: {str(e)}")
            raise e
    
    def _extract_scenes(self, script: str) -> list:
        """
        Extract scene descriptions from the script
        """
        scene_pattern = r'Scene:\s*([^\n]+)'
        scenes = re.findall(scene_pattern, script, re.IGNORECASE)
        return [scene.strip() for scene in scenes if scene.strip()]
    
    def _extract_narrator_text(self, script: str) -> str:
        """
        Extract narrator text for audio generation
        """
        narrator_pattern = r'Narrator:\s*([^]*?)(?=\n\n|Scene:|$)'
        narrator_matches = re.findall(narrator_pattern, script, re.IGNORECASE)
        
        if narrator_matches:
            narrator_text = ' '.join([match.strip() for match in narrator_matches])
            # Clean up the text
            narrator_text = re.sub(r'\s+', ' ', narrator_text).strip()
            return narrator_text
        else:
            # Fallback: return the entire script
            return script
    
    async def generate_multiple_scripts(self, news_articles: list) -> list:
        """
        Generate scripts for multiple news articles
        """
        scripts = []
        
        for article in news_articles:
            try:
                script_data = await self.generate_reel_script(
                    news_title=article['title'],
                    news_content=article['description'],
                    news_url=article['url']
                )
                
                scripts.append({
                    'article': article,
                    'script_data': script_data
                })
                
            except Exception as e:
                print(f"Error generating script for article '{article['title']}': {str(e)}")
                continue
        
        return scripts 