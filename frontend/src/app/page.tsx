'use client'

import { useState, useEffect } from 'react'
import VideoCard from './components/VideoCard'
import Sidebar from './components/Sidebar'
import { ApiService, NewsReel } from './services/api'

export default function Home() {
  const [reels, setReels] = useState<NewsReel[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchReels()
  }, [])

  const fetchReels = async () => {
    try {
      setLoading(true)
      setError(null)
      
      console.log('Fetching trending reels from API...')
      const newsReels = await ApiService.getTrendingReels()
      
      console.log('Received reels:', newsReels)
      setReels(newsReels)
    } catch (err) {
      console.error('Error fetching reels:', err)
      setError('Failed to load news reels')
    } finally {
      setLoading(false)
    }
  }

  const generateCustomReel = async (topic: string) => {
    try {
      setLoading(true)
      const customReel = await ApiService.generateCustomReel(topic)
      
      if (customReel) {
        setReels(prev => [customReel, ...prev])
      }
    } catch (err) {
      console.error('Error generating custom reel:', err)
      setError('Failed to generate custom reel')
    } finally {
      setLoading(false)
    }
  }

  const handleTopicSelect = (topic: string) => {
    generateCustomReel(topic)
  }

  if (loading && reels.length === 0) {
    return (
      <div className="app">
        <div className="app__header">
          <h1 className="app__title">Factually</h1>
        </div>
        <div className="app__loading">
          <div className="loading__spinner"></div>
          <p>Loading news reels...</p>
        </div>
      </div>
    )
  }

  if (error && reels.length === 0) {
    return (
      <div className="app">
        <div className="app__header">
          <h1 className="app__title">Factually</h1>
        </div>
        <div className="app__error">
          <p>{error}</p>
          <button onClick={fetchReels} className="error__retry">
            Try Again
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="app">
      <div className="app__header">
        <h1 className="app__title">Factually</h1>
      </div>
      
      <div className="app__content">
        <Sidebar onTopicSelect={handleTopicSelect} loading={loading} />
        
        <div className="app__main">
          <div className="app__videos">
            {reels.length === 0 ? (
              <div style={{ 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center', 
                height: '100%', 
                color: 'white',
                fontSize: '18px'
              }}>
                <p>No reels available. Try clicking a topic in the sidebar!</p>
              </div>
            ) : (
              reels.map((reel) => (
                <VideoCard
                  key={reel.id}
                  url={reel.videoUrl}
                  title={reel.title}
                  description={reel.description}
                  audioUrl={reel.audioUrl}
                  script={reel.script}
                  source={reel.source}
                  isNewsReel={true}
                  channel="Factually"
                  avatarSrc="https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face"
                  song="News Audio"
                  likes={Math.floor(Math.random() * 1000)}
                  shares={Math.floor(Math.random() * 100)}
                />
              ))
            )}
          </div>
          
          {loading && reels.length > 0 && (
            <div className="app__loadingMore">
              <div className="loading__spinner"></div>
              <p>Loading more reels...</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
