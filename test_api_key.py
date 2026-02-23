#!/usr/bin/env python3
import requests
import os

TMDB_API_KEY = "b6871583efed647aad18826d6abbca01"
BASE_URL = 'https://api.themoviedb.org/3'

def test_api_key():
    """测试 API Key 是否有效"""
    print("🔍 测试 TMDB API Key...")
    
    # 测试获取配置信息（不需要额外参数）
    url = f'{BASE_URL}/configuration'
    params = {
        'api_key': TMDB_API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Key 有效！")
            print(f"📊 响应数据: {data.get('images', {}).get('base_url', 'N/A')}")
            return True
        elif response.status_code == 401:
            print("❌ API Key 无效或已过期")
            print(f"错误信息: {response.text}")
            return False
        else:
            print(f"⚠️ 其他错误: {response.status_code}")
            print(f"响应: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def test_movie_search():
    """测试电影搜索功能"""
    print("\n🎬 测试电影搜索...")
    
    url = f'{BASE_URL}/search/movie'
    params = {
        'api_key': TMDB_API_KEY,
        'query': 'Inception',
        'language': 'zh-TW',
        'page': 1
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 搜索成功！找到 {data.get('total_results', 0)} 个结果")
            if data.get('results'):
                movie = data['results'][0]
                print(f"  电影: {movie.get('title')} ({movie.get('release_date', 'N/A')})")
                print(f"  评分: {movie.get('vote_average')}")
            return True
        else:
            print(f"❌ 搜索失败: {response.status_code}")
            print(f"错误: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ 搜索请求失败: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("TMDB API Key 测试")
    print("=" * 50)
    
    # 测试 API Key
    api_valid = test_api_key()
    
    if api_valid:
        # 测试搜索功能
        test_movie_search()
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)