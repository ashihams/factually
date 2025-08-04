from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# Import our services
try:
    from services.news_service import NewsService
    from services.script_service import ScriptService
    from services.audio_service import AudioService
    from services.video_service import VideoService
    SERVICES_AVAILABLE = True
except ImportError:
    SERVICES_AVAILABLE = False

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Factually News Reels API",
    description="API for generating news-based short-form video content",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"]
,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for audio
os.makedirs("static/audio", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize services only if available
if SERVICES_AVAILABLE:
    try:
        news_service = NewsService()
        script_service = ScriptService()
        audio_service = AudioService()
        video_service = VideoService()
    except Exception as e:
        print(f"Error initializing services: {e}")
        SERVICES_AVAILABLE = False

# Pydantic models
class NewsRequest(BaseModel):
    category: Optional[str] = "general"
    country: Optional[str] = "us"
    page_size: Optional[int] = 10

class ScriptRequest(BaseModel):
    news_title: str
    news_content: str
    news_url: str

class AudioRequest(BaseModel):
    script: str
    voice: Optional[str] = "default"

class VideoRequest(BaseModel):
    prompts: List[str]

class ReelRequest(BaseModel):
    category: Optional[str] = "general"
    country: Optional[str] = "us"
    count: Optional[int] = 5

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Factually News Reels API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is operational"}

# Test endpoint that works without API keys
@app.get("/test-reels")
async def get_test_reels():
    """
    Get test reels that work without API keys
    """
    test_reels = [
        {
            "id": "test-1",
            "title": "Breaking News: AI Breakthrough in Healthcare",
            "description": "Scientists have developed a revolutionary AI system that can diagnose diseases with 95% accuracy, potentially saving millions of lives worldwide.",
            "videoUrl": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
            "audioUrl": None,
            "script": "Today, we bring you breaking news about a revolutionary AI breakthrough that could change healthcare forever. Scientists have developed an artificial intelligence system with unprecedented accuracy in disease diagnosis.",
            "duration": "60 seconds",
            "source": "Tech News Daily",
            "publishedAt": "2024-08-03T10:00:00Z"
        },
        {
            "id": "test-2",
            "title": "Climate Change: Global Action Plan Announced",
            "description": "World leaders have announced a comprehensive plan to combat climate change, including massive investments in renewable energy and carbon capture technology.",
            "videoUrl": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
            "audioUrl": None,
            "script": "In a historic moment, world leaders have come together to announce a comprehensive global action plan to combat climate change. This unprecedented initiative includes massive investments in renewable energy.",
            "duration": "60 seconds",
            "source": "Environmental News",
            "publishedAt": "2024-08-03T09:30:00Z"
        },
        {
            "id": "test-3",
            "title": "Space Exploration: New Mars Mission Discoveries",
            "description": "NASA's latest Mars mission has uncovered evidence of ancient water systems and potential signs of microbial life on the red planet.",
            "videoUrl": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
            "audioUrl": None,
            "script": "NASA's latest Mars mission has made groundbreaking discoveries that could change our understanding of the red planet. Scientists have found evidence of ancient water systems and potential signs of microbial life.",
            "duration": "60 seconds",
            "source": "Space News",
            "publishedAt": "2024-08-03T09:00:00Z"
        }
    ]
    
    return {
        "reels": test_reels,
        "count": len(test_reels),
        "status": "success",
        "message": "Test reels loaded successfully"
    }

# News endpoint
@app.post("/news")
async def get_news(request: NewsRequest):
    """
    Fetch news from NewsAPI based on category and country
    """
    if not SERVICES_AVAILABLE:
        raise HTTPException(status_code=503, detail="News service not available - API keys required")
    
    try:
        articles = await news_service.get_top_headlines(
            category=request.category,
            country=request.country,
            page_size=request.page_size
        )
        return {"articles": articles, "count": len(articles)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Script generation endpoint
@app.post("/generate-script")
async def generate_script(request: ScriptRequest):
    """
    Generate 1-minute reel script using Gemini API
    """
    if not SERVICES_AVAILABLE:
        raise HTTPException(status_code=503, detail="Script service not available - API keys required")
    
    try:
        script_data = await script_service.generate_reel_script(
            news_title=request.news_title,
            news_content=request.news_content,
            news_url=request.news_url
        )
        return script_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Audio generation endpoint
@app.post("/generate-audio")
async def generate_audio(request: AudioRequest):
    """
    Generate voice-over audio using ElevenLabs API
    """
    if not SERVICES_AVAILABLE:
        raise HTTPException(status_code=503, detail="Audio service not available - API keys required")
    
    try:
        audio_data = await audio_service.generate_audio(request.script)
        return audio_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Video fetching endpoint
@app.post("/fetch-videos")
async def fetch_videos(request: VideoRequest):
    """
    Fetch relevant videos from Pexels API
    """
    if not SERVICES_AVAILABLE:
        raise HTTPException(status_code=503, detail="Video service not available - API keys required")
    
    try:
        videos = await video_service.fetch_videos(request.prompts)
        return {"videos": videos, "count": len(videos)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Complete pipeline endpoint
@app.post("/generate-reel")
async def generate_reel(request: ReelRequest):
    """
    Complete pipeline: News → Script → Audio → Videos
    """
    if not SERVICES_AVAILABLE:
        # Return test reel instead
        test_reel = {
            "id": f"generated-{request.category}-{request.count}",
            "title": f"{request.category.title()} News Update",
            "description": f"Latest {request.category} news and developments from around the world",
            "videoUrl": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
            "audioUrl": None,
            "script": f"Today we bring you the latest {request.category} news and developments from around the world.",
            "duration": "60 seconds",
            "source": f"{request.category.title()} News",
            "publishedAt": "2024-08-03T10:00:00Z"
        }
        
        return {
            "reels": [test_reel],
            "count": 1,
            "status": "success",
            "message": "Test reel generated (API keys required for real generation)"
        }
    
    try:
        # Step 1: Fetch news
        articles = await news_service.get_top_headlines(
            category=request.category,
            country=request.country,
            page_size=request.count
        )
        
        if not articles:
            raise HTTPException(status_code=404, detail="No news articles found")
        
        # Step 2: Generate scripts for each article
        scripts = await script_service.generate_multiple_scripts(articles)
        
        # Step 3: Generate audio for each script
        audio_results = await audio_service.generate_multiple_audio(scripts)
        
        # Step 4: Fetch videos for each script
        video_results = await video_service.fetch_multiple_videos(audio_results)
        
        # Step 5: Compile final results
        final_reels = []
        for result in video_results:
            reel = {
                'article': result['article'],
                'script': result['script_data'],
                'audio': result['script_data'].get('audio_data'),
                'videos': result['video_data']['videos'],
                'reel_data': {
                    'title': result['article']['title'],
                    'description': result['article']['description'],
                    'script': result['script_data']['script'],
                    'audio_url': result['script_data'].get('audio_data', {}).get('audio_url'),
                    'video_urls': [v['url'] for v in result['video_data']['videos']],
                    'duration': result['script_data'].get('estimated_duration', '60 seconds')
                }
            }
            final_reels.append(reel)
        
        return {
            "reels": final_reels,
            "count": len(final_reels),
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trending-reels")
async def get_trending_reels():
    print("🚀 Hit /trending-reels endpoint")
    
    if not SERVICES_AVAILABLE:
        print("❗ SERVICES_AVAILABLE is False → returning test reels")
        return await get_test_reels()

    try:
        print("📥 Attempting to call news_service.get_trending_news()...")

        if not hasattr(news_service, "get_trending_news"):
            raise Exception("⚠️ 'get_trending_news' method is missing in NewsService class!")

        articles = await news_service.get_trending_news(page_size=10)
        print(f"✅ Received {len(articles)} articles")

        # Continue your original logic
        scripts = await script_service.generate_multiple_scripts(articles)
        audio_results = await audio_service.generate_multiple_audio(scripts)
        video_results = await video_service.fetch_multiple_videos(audio_results)

        trending_reels = []
        for result in video_results:
            reel = {
                'article': result['article'],
                'script': result['script_data'],
                'audio': result['script_data'].get('audio_data'),
                'videos': result['video_data']['videos'],
                'reel_data': {
                    'title': result['article']['title'],
                    'description': result['article']['description'],
                    'script': result['script_data']['script'],
                    'audio_url': result['script_data'].get('audio_data', {}).get('audio_url'),
                    'video_urls': [v['url'] for v in result['video_data']['videos']],
                    'duration': result['script_data'].get('estimated_duration', '60 seconds')
                }
            }
            trending_reels.append(reel)

        return {
            "reels": trending_reels,
            "count": len(trending_reels),
            "status": "success"
        }

    except Exception as e:
        print(f"🔥 Exception in /trending-reels: {e}")
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002) 