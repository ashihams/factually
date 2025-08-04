#!/usr/bin/env python3
"""
Quick start script for Factually News Reels API
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = [
        'NEWSAPI_KEY',
        'GEMINI_API_KEY', 
        'ELEVENLABS_API_KEY',
        'PEXELS_API_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease check your .env file!")
        return False
    
    print("✅ All environment variables are set!")
    return True

def main():
    print("🚀 Starting Factually News Reels API...")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        return
    
    print("\n📡 Server will be available at:")
    print("   - API: http://localhost:8000")
    print("   - Docs: http://localhost:8000/docs")
    print("   - ReDoc: http://localhost:8000/redoc")
    
    print("\n🎯 Available endpoints:")
    print("   - GET  /health - Health check")
    print("   - POST /news - Fetch news")
    print("   - POST /generate-script - Generate script")
    print("   - POST /generate-audio - Generate audio")
    print("   - POST /fetch-videos - Fetch videos")
    print("   - POST /generate-reel - Complete pipeline")
    print("   - GET  /trending-reels - Trending reels")
    
    print("\n🔥 Starting server...")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    # Start the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main() 