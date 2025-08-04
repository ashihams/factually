import requests
import json

# Test the API endpoints
BASE_URL = "http://localhost:8001"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_news():
    """Test news endpoint"""
    try:
        data = {
            "category": "technology",
            "country": "us",
            "page_size": 3
        }
        response = requests.post(f"{BASE_URL}/news", json=data)
        print(f"✅ News endpoint: {response.status_code}")
        result = response.json()
        print(f"Found {result.get('count', 0)} articles")
        if result.get('articles'):
            print(f"First article: {result['articles'][0]['title'][:50]}...")
        return True
    except Exception as e:
        print(f"❌ News endpoint failed: {e}")
        return False

def test_script_generation():
    """Test script generation"""
    try:
        data = {
            "news_title": "AI Breakthrough in Medical Diagnosis",
            "news_content": "Scientists have developed a new AI system that can diagnose diseases with 95% accuracy, potentially revolutionizing healthcare worldwide.",
            "news_url": "https://example.com/ai-medical"
        }
        response = requests.post(f"{BASE_URL}/generate-script", json=data)
        print(f"✅ Script generation: {response.status_code}")
        result = response.json()
        print(f"Script word count: {result.get('word_count', 0)}")
        print(f"Estimated duration: {result.get('estimated_duration', 'N/A')}")
        return True
    except Exception as e:
        print(f"❌ Script generation failed: {e}")
        return False

def test_trending_reels():
    """Test trending reels endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/trending-reels")
        print(f"✅ Trending reels: {response.status_code}")
        result = response.json()
        print(f"Generated {result.get('count', 0)} reels")
        return True
    except Exception as e:
        print(f"❌ Trending reels failed: {e}")
        return False

def main():
    print("🧪 Testing Factually News Reels API...")
    print("=" * 50)
    
    # Test each endpoint
    tests = [
        ("Health Check", test_health),
        ("News Fetching", test_news),
        ("Script Generation", test_script_generation),
        ("Trending Reels", test_trending_reels)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed")

if __name__ == "__main__":
    main() 