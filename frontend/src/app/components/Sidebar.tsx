'use client'

import React from 'react'

interface SidebarProps {
  onTopicSelect: (topic: string) => void
  loading: boolean
}

const Sidebar: React.FC<SidebarProps> = ({ onTopicSelect, loading }) => {
  const topics = [
    { id: 'community-resilience', name: 'Community Resilience', icon: '🏘️' },
    { id: 'disaster-recovery', name: 'Disaster Recovery', icon: '🌪️' },
    { id: 'local-heroes', name: 'Local Heroes', icon: '🦸' },
    { id: 'neighborhood-support', name: 'Neighborhood Support', icon: '🤝' },
    { id: 'environmental-action', name: 'Environmental Action', icon: '🌱' },
    { id: 'social-justice', name: 'Social Justice', icon: '⚖️' },
    { id: 'education-initiatives', name: 'Education Initiatives', icon: '📚' },
    { id: 'health-wellness', name: 'Health & Wellness', icon: '🏥' },
    { id: 'economic-development', name: 'Economic Development', icon: '💼' },
    { id: 'cultural-preservation', name: 'Cultural Preservation', icon: '🏛️' },
    { id: 'technology-innovation', name: 'Technology Innovation', icon: '💻' },
    { id: 'sports-community', name: 'Sports & Community', icon: '⚽' }
  ]

  return (
    <div className="sidebar">
      <div className="sidebar__header">
        <h3>News Topics</h3>
        <p>Generate reels by topic</p>
      </div>
      
      <div className="sidebar__topics">
        {topics.map((topic) => (
          <button
            key={topic.id}
            className="sidebar__topic-button"
            onClick={() => onTopicSelect(topic.id)}
            disabled={loading}
          >
            <span className="topic__icon">{topic.icon}</span>
            <span className="topic__name">{topic.name}</span>
            {loading && <div className="topic__loading"></div>}
          </button>
        ))}
      </div>
      
      <div className="sidebar__footer">
        <p>Click any topic to generate a custom news reel</p>
      </div>
    </div>
  )
}

export default Sidebar 