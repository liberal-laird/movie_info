#!/usr/bin/env python3
import requests

TMDB_API_KEY = "b6871583efed647aad18826d6abbca01"
BASE_URL = 'https://api.themoviedb.org/3'
LANGUAGE = 'zh-TW'

def test_now_playing():
    """测试正在上映的电影API"""
    print("🎬 测试正在上映的电影API...")
    
    url = f'{BASE_URL}/movie/now_playing'
    
    for page in range(1, 4):
        print(f"\n📄 测试第 {page} 页...")
        params = {
            'api_key': TMDB_API_KEY,
            'language': LANGUAGE,
            'page': page
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            print(f"  状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"  成功！第 {page} 页有 {len(data.get('results', []))} 部电影")
                if data.get('results'):
                    movie = data['results'][0]
                    print(f"  示例电影: {movie.get('title')} (ID: {movie.get('id')})")
            else:
                print(f"  失败: {response.status_code}")
                print(f"  错误: {response.text[:200]}")
                
        except Exception as e:
            print(f"  请求失败: {e}")

if __name__ == "__main__":
    test_now_playing()