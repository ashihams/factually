'use client'

import React, { useRef, useState, useEffect } from 'react'
import VideoHeader from './VideoHeader'
import VideoFooter from './VideoFooter'

interface VideoCardProps {
  url: string
  likes?: number
  shares?: number
  avatarSrc?: string
  song?: string
  channel?: string
  // News reel specific props
  title?: string
  description?: string
  audioUrl?: string
  script?: string
  source?: string
  isNewsReel?: boolean
}

const VideoCard: React.FC<VideoCardProps> = ({ 
  url, 
  likes = 0, 
  shares = 0, 
  avatarSrc = "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face",
  song = "News Audio",
  channel = "Factually",
  title,
  description,
  audioUrl,
  script,
  source,
  isNewsReel = false
}) => {
  const [isVideoPlaying, setIsVideoPlaying] = useState(false)
  const [isAudioPlaying, setIsAudioPlaying] = useState(false)
  const videoRef = useRef<HTMLVideoElement>(null)
  const audioRef = useRef<HTMLAudioElement>(null)

  const onVideoPress = () => {
    if (isVideoPlaying) {
      videoRef.current?.pause()
      audioRef.current?.pause()
      setIsVideoPlaying(false)
      setIsAudioPlaying(false)
    } else {
      videoRef.current?.play()
      if (audioUrl && audioRef.current) {
        audioRef.current.play()
        setIsAudioPlaying(true)
      }
      setIsVideoPlaying(true)
    }
  }

  // Handle video end
  useEffect(() => {
    const video = videoRef.current
    if (!video) return

    const handleVideoEnd = () => {
      setIsVideoPlaying(false)
      if (audioRef.current) {
        audioRef.current.pause()
        setIsAudioPlaying(false)
      }
    }

    video.addEventListener('ended', handleVideoEnd)
    return () => video.removeEventListener('ended', handleVideoEnd)
  }, [])

  // Handle audio end
  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    const handleAudioEnd = () => {
      setIsAudioPlaying(false)
    }

    audio.addEventListener('ended', handleAudioEnd)
    return () => audio.removeEventListener('ended', handleAudioEnd)
  }, [])

  return (
    <div className="videoCard">
      <VideoHeader />
      <video
        ref={videoRef}
        onClick={onVideoPress}
        className="videoCard__player"
        src={url}
        loop
        muted
        playsInline
      />
      
      {/* Audio element for news reels */}
      {audioUrl && (
        <audio
          ref={audioRef}
          src={`http://localhost:8001${audioUrl}`}
          preload="metadata"
        />
      )}
      
      {/* News overlay for news reels */}
      {isNewsReel && title && (
        <div className="videoCard__newsOverlay">
          <div className="videoCard__newsInfo">
            <h3 className="videoCard__newsTitle">{title}</h3>
            {description && (
              <p className="videoCard__newsDescription">{description}</p>
            )}
            {source && (
              <span className="videoCard__newsSource">Source: {source}</span>
            )}
          </div>
        </div>
      )}
      
      <VideoFooter
        channel={channel}
        avatarSrc={avatarSrc}
        song={song}
        likes={likes}
        shares={shares}
      />
    </div>
  )
}

export default VideoCard 