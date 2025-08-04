import requests
import os
from typing import List, Dict, Any
from datetime import datetime, timedelta

class NewsService:
    def __init__(self):
        self.api_key = os.getenv('NEWSAPI_KEY')
        self.base_url = "https://newsapi.org/v2"
    
    async def get_top_headlines(self, category: str = "general", country: str = "us", page_size: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch top headlines from NewsAPI
        """
        try:
            url = f"{self.base_url}/top-headlines"
            params = {
                'country': country,
                'category': category,
                'pageSize': page_size,
                'apiKey': self.api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'ok':
                articles = data['articles']
                # Filter out articles without content
                filtered_articles = []
                for article in articles:
                    if article.get('title') and article.get('description') and article.get('url'):
                        filtered_articles.append({
                            'title': article['title'],
                            'description': article['description'],
                            'content': article.get('content', ''),
                            'url': article['url'],
                            'urlToImage': article.get('urlToImage', ''),
                            'publishedAt': article.get('publishedAt', ''),
                            'source': article.get('source', {}).get('name', 'Unknown'),
                            'author': article.get('author', 'Unknown')
                        })
                return filtered_articles
            else:
                raise Exception(f"NewsAPI error: {data.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"Error fetching news: {str(e)}")
            raise e
    
    async def get_trending_news(self, page_size: int = 10) -> List[Dict[str, Any]]:
        """
        Get trending news from multiple categories
        """
        categories = ['technology', 'business', 'entertainment', 'sports', 'science']
        all_articles = []
        
        for category in categories:
            try:
                articles = await self.get_top_headlines(category=category, page_size=2)
                all_articles.extend(articles)
            except Exception as e:
                print(f"Error fetching {category} news: {str(e)}")
                continue
        
        # Sort by published date and return top articles
        all_articles.sort(key=lambda x: x.get('publishedAt', ''), reverse=True)
        return all_articles[:page_size]
    
    async def get_news_by_keyword(self, keyword: str, page_size: int = 10) -> List[Dict[str, Any]]:
        """
        Search news by keyword
        """
        try:
            url = f"{self.base_url}/everything"
            params = {
                'q': keyword,
                'pageSize': page_size,
                'sortBy': 'publishedAt',
                'language': 'en',
                'apiKey': self.api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'ok':
                articles = data['articles']
                filtered_articles = []
                for article in articles:
                    if article.get('title') and article.get('description') and article.get('url'):
                        filtered_articles.append({
                            'title': article['title'],
                            'description': article['description'],
                            'content': article.get('content', ''),
                            'url': article['url'],
                            'urlToImage': article.get('urlToImage', ''),
                            'publishedAt': article.get('publishedAt', ''),
                            'source': article.get('source', {}).get('name', 'Unknown'),
                            'author': article.get('author', 'Unknown')
                        })
                return filtered_articles
            else:
                raise Exception(f"NewsAPI error: {data.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"Error searching news: {str(e)}")
            raise e 