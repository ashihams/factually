// API service for communicating with the FastAPI backend

const API_BASE_URL = 'http://localhost:8000';

export interface NewsReel {
  id: string;
  title: string;
  description: string;
  videoUrl: string;
  audioUrl?: string;
  script: string;
  duration: string;
  source: string;
  publishedAt: string;
}

export interface ApiResponse {
  reels: NewsReel[];
  count: number;
  status: string;
}

export class ApiService {
  static async getTrendingReels(): Promise<NewsReel[]> {
    try {
      console.log('Fetching from:', `${API_BASE_URL}/trending-reels`);
      const response = await fetch(`${API_BASE_URL}/trending-reels`);
      
      console.log('Response status:', response.status);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data: ApiResponse = await response.json();
      console.log('API Response:', data);
      
      // Transform the API response to match our frontend format
      return data.reels.map((reel, index) => ({
        id: reel.id || `reel-${index}`,
        title: reel.title,
        description: reel.description,
        videoUrl: reel.videoUrl,
        audioUrl: reel.audioUrl,
        script: reel.script,
        duration: reel.duration,
        source: reel.source,
        publishedAt: reel.publishedAt
      }));
    } catch (error) {
      console.error('Error fetching trending reels:', error);
      console.log('Using fallback data...');
      // Return fallback data if API fails
      return this.getFallbackReels();
    }
  }

  static async generateCustomReel(category: string = 'technology'): Promise<NewsReel | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/generate-reel`, {
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
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data: ApiResponse = await response.json();
      
      if (data.reels && data.reels.length > 0) {
        const reel = data.reels[0];
        return {
          id: reel.id || 'custom-reel',
          title: reel.title,
          description: reel.description,
          videoUrl: reel.videoUrl,
          audioUrl: reel.audioUrl,
          script: reel.script,
          duration: reel.duration,
          source: reel.source,
          publishedAt: reel.publishedAt
        };
      }
      
      return null;
    } catch (error) {
      console.error('Error generating custom reel:', error);
      return null;
    }
  }

  // Fallback data in case API is not available
  private static getFallbackReels(): NewsReel[] {
    return [
      {
        id: 'fallback-1',
        title: 'Breaking News: AI Breakthrough',
        description: 'Scientists discover new AI technology that could revolutionize healthcare',
        videoUrl: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
        script: 'Today, we bring you breaking news about a revolutionary AI breakthrough...',
        duration: '60 seconds',
        source: 'Tech News',
        publishedAt: new Date().toISOString()
      },
      {
        id: 'fallback-2',
        title: 'Climate Change Update',
        description: 'Latest developments in global climate initiatives',
        videoUrl: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4',
        script: 'The world is taking action against climate change...',
        duration: '60 seconds',
        source: 'Environmental News',
        publishedAt: new Date().toISOString()
      }
    ];
  }
} 