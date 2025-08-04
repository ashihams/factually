'use client'

import React from 'react'
import ArrowBackIosOutlinedIcon from '@mui/icons-material/ArrowBackIosOutlined'
import CameraAltOutlinedIcon from '@mui/icons-material/CameraAltOutlined'

const VideoHeader: React.FC = () => {
  return (
    <div className="videoHeader">
      <ArrowBackIosOutlinedIcon />
      <h3>Reels</h3>
      <CameraAltOutlinedIcon />
    </div>
  )
}

export default VideoHeader 