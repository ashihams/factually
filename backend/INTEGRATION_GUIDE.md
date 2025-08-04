# Factually Backend Integration Guide

## 🚀 Backend Status: READY

Your FastAPI backend is now fully functional with all services integrated:

### ✅ **Completed Services:**
- **NewsService**: Fetches world news from NewsAPI
- **ScriptService**: Generates 1-minute reel scripts using Gemini API
- **AudioService**: Creates voice-over audio using ElevenLabs API
- **VideoService**: Fetches relevant videos from Pexels API

### 🔗 **Available Endpoints:**

#### **Health & Status**
- `GET /` - Root endpoint
- `GET /health` - Health check

#### **Individual Services**
- `POST /news` - Fetch news articles
- `POST /generate-script` - Generate reel script
- `POST /generate-audio` - Generate voice-over
- `POST /fetch-videos` - Fetch stock videos

#### **Complete Pipeline**
- `POST /generate-reel` - Full pipeline (News → Script → Audio → Videos)
- `GET /trending-reels` - Get trending news reels

## 🔧 **Frontend Integration**

### **1. Update Your Frontend API Calls**

Replace your current video fetching with news-based reels:

```typescript
// In your frontend, replace random videos with news reels
const fetchNewsReels = async () => {
  try {
    const response = await fetch('http://localhost:8000/trending-reels');
    const data = await response.json();
    
    // Transform the data for your frontend
    const reels = data.reels.map(reel => ({
      id: reel.article.url,
      videoUrl: reel.video_data.videos[0]?.url || '',
      audioUrl: reel.audio_data?.audio_url || '',
      title: reel.article.title,
      description: reel.article.description,
      script: reel.script_data.script,
      duration: reel.script_data.estimated_duration
    }));
    
    return reels;
  } catch (error) {
    console.error('Error fetching news reels:', error);
    return [];
  }
};
```

### **2. Enhanced Video Component**

Update your video component to handle audio:

```typescript
const VideoPlayer = ({ reel }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const videoRef = useRef(null);
  const audioRef = useRef(null);

  const handlePlay = () => {
    if (videoRef.current && audioRef.current) {
      videoRef.current.play();
      audioRef.current.play();
      setIsPlaying(true);
    }
  };

  const handlePause = () => {
    if (videoRef.current && audioRef.current) {
      videoRef.current.pause();
      audioRef.current.pause();
      setIsPlaying(false);
    }
  };

  return (
    <div className="relative">
      <video
        ref={videoRef}
        src={reel.videoUrl}
        className="w-full h-full object-cover"
        loop
        muted
        onPlay={() => setIsPlaying(true)}
        onPause={() => setIsPlaying(false)}
      />
      
      {/* Audio element for voice-over */}
      <audio
        ref={audioRef}
        src={`http://localhost:8000${reel.audioUrl}`}
        onEnded={() => setIsPlaying(false)}
      />
      
      {/* Play/Pause button */}
      <button
        onClick={isPlaying ? handlePause : handlePlay}
        className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
      >
        {isPlaying ? '⏸️' : '▶️'}
      </button>
      
      {/* News info overlay */}
      <div className="absolute bottom-4 left-4 text-white">
        <h3 className="text-lg font-bold">{reel.title}</h3>
        <p className="text-sm opacity-90">{reel.description}</p>
      </div>
    </div>
  );
};
```

### **3. Generate Custom Reels**

Add a feature to generate reels for specific topics:

```typescript
const generateCustomReel = async (category = 'technology') => {
  try {
    const response = await fetch('http://localhost:8000/generate-reel', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        category: category,
        country: 'us',
        count: 1
      })
    });
    
    const data = await response.json();
    return data.reels[0]; // Return the first generated reel
  } catch (error) {
    console.error('Error generating custom reel:', error);
    return null;
  }
};
```

## 🎯 **Quality Features**

### **High-Quality Scripts**
- 1-minute duration (150-160 words)
- Professional structure with scenes
- Engaging hooks and CTAs
- Nas Daily-style storytelling

### **Professional Audio**
- ElevenLabs AI voices
- Natural-sounding narration
- Optimized for social media

### **Relevant Videos**
- Pexels stock videos
- Portrait orientation for mobile
- Scene-matched content
- High-quality resolution

## 🚀 **Next Steps**

1. **Test the API**: Run `python test_api.py` to verify all endpoints
2. **Update Frontend**: Integrate the new endpoints into your Next.js app
3. **Customize**: Adjust script prompts, voice settings, or video preferences
4. **Deploy**: Ready for production deployment

## 📊 **API Response Format**

```json
{
  "reels": [
    {
      "article": {
        "title": "News Title",
        "description": "News description",
        "url": "https://...",
        "source": "Source Name"
      },
      "script_data": {
        "script": "Full script with scenes",
        "scenes": ["Scene descriptions"],
        "narrator_text": "Clean text for TTS",
        "word_count": 150,
        "estimated_duration": "60 seconds"
      },
      "audio_data": {
        "audio_url": "/static/audio/filename.mp3",
        "duration": 60.0,
        "voice_id": "voice_id"
      },
      "video_data": {
        "videos": [
          {
            "url": "https://video-url.mp4",
            "width": 1920,
            "height": 1080,
            "duration": 30
          }
        ]
      }
    }
  ],
  "count": 1,
  "status": "success"
}
```

Your backend is now ready to generate professional-quality news reels! 🎉 