# Factually News Reels API

FastAPI backend for generating news-based short-form video content.

## Features

- **News Fetching**: Get world news from NewsAPI
- **Script Generation**: Create 1-minute reel scripts using Gemini API
- **Audio Generation**: Generate voice-over using ElevenLabs API
- **Video Fetching**: Get relevant videos from Pexels API
- **Complete Pipeline**: End-to-end news-to-reel generation

## API Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check

### Core Endpoints
- `POST /news` - Fetch news articles
- `POST /generate-script` - Generate reel script from news
- `POST /generate-audio` - Generate voice-over audio
- `POST /fetch-videos` - Fetch relevant videos
- `POST /generate-reel` - Complete pipeline

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Copy .env file** from main_code to backend folder

3. **Run the server:**
   ```bash
   python main.py
   ```
   or
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access API docs:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Environment Variables

Required in `.env` file:
- `NEWSAPI_KEY`
- `GEMINI_API_KEY`
- `ELEVENLABS_API_KEY`
- `PEXELS_API_KEY`
- `YOUTUBE_API_KEY`
- `GROQ_API_KEY`

## Usage

The API will be available at `http://localhost:8000` and can be integrated with your Next.js frontend. 