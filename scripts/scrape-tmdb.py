#!/usr/bin/env python3
"""
TMDb Movie Scraper for Hugo
爬取 TMDb 電影，生成 Hugo Markdown 文件
"""

import os
import sys
import json
import requests
import urllib.parse
from datetime import datetime, timedelta

# 配置
TMDB_API_KEY = os.environ.get('TMDB_API_KEY', '')
BASE_URL = 'https://api.themoviedb.org/3'
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', 'content/posts')
POSTER_DIR = os.environ.get('POSTER_DIR', 'static/posters')
LANGUAGE = 'zh-TW'
POSTER_BASE_URL = 'https://image.tmdb.org/t/p/w500'

def get_headers():
    return {
        'api_key': TMDB_API_KEY
    }

def search_movie(query):
    """搜索電影"""
    url = f'{BASE_URL}/search/movie'
    params = {
        'api_key': TMDB_API_KEY,
        'query': query,
        'language': LANGUAGE,
        'page': 1
    }
    response = requests.get(url, params=params)
    return response.json()

def get_movie_details(movie_id):
    """獲取電影詳情"""
    url = f'{BASE_URL}/movie/{movie_id}'
    params = {
        'api_key': TMDB_API_KEY,
        'language': LANGUAGE,
        'append_to_response': 'credits,images'
    }
    response = requests.get(url, params=params)
    return response.json()

def get_english_title(movie_data):
    """獲取英文標題（原始標題）"""
    return movie_data.get('original_title', '') or movie_data.get('title', '')

def get_chinese_title(movie_data):
    """獲取中文標題"""
    return movie_data.get('title', '') or movie_data.get('original_title', '')

def get_genres(movie_data):
    """獲取類型"""
    genres = movie_data.get('genres', [])
    return [g['name'] for g in genres]

def get_cast(movie_data, count=5):
    """獲取主要演員"""
    cast = movie_data.get('credits', {}).get('cast', [])[:count]
    result = []
    for actor in cast:
        result.append({
            'name': actor.get('name', ''),
            'character': actor.get('character', ''),
            'profile_path': actor.get('profile_path', '')
        })
    return result

def download_poster(poster_path, movie_id):
    """下載海報"""
    if not poster_path:
        return None
    url = f'{POSTER_BASE_URL}{poster_path}'
    response = requests.get(url)
    if response.status_code == 200:
        filename = f'{movie_id}{os.path.splitext(poster_path)[1]}'
        filepath = os.path.join(POSTER_DIR, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return f'/posters/{filename}'
    return None

def generate_frontmatter(movie_data, poster_url):
    """生成 Hugo frontmatter"""
    chinese_title = get_chinese_title(movie_data)
    english_title = get_english_title(movie_data)
    release_date = movie_data.get('release_date', '')
    
    # 評分
    vote_average = movie_data.get('vote_average', 0)
    vote_count = movie_data.get('vote_count', 0)
    
    # 類型
    genres = get_genres(movie_data)
    
    # 演員
    cast = get_cast(movie_data, 8)
    cast_list = []
    for actor in cast:
        name = actor['name']
        if name:
            cast_list.append(name)
    
    frontmatter = f'''---
title: "{chinese_title}"
originalTitle: "{english_title}"
date: {release_date}T00:00:00+08:00
draft: false
Cover: "{poster_url or ''}"
categories: {json.dumps(genres)}
tags: {json.dumps(genres)}
rating: {vote_average}
ratingCount: {vote_count}
plot: "{movie_data.get('overview', '')}"
imdbId: "{movie_data.get('imdb_id', '')}"
tmdbId: {movie_data.get('id', 0)}
---

'''
    return frontmatter, chinese_title, english_title

def generate_markdown(movie_data, poster_url, output_file):
    """生成完整的 Markdown 文件"""
    frontmatter, chinese_title, english_title = generate_frontmatter(movie_data, poster_url)
    
    # 在内容开头添加海报图片
    content = f'![Poster]({poster_url})\n\n' if poster_url else ''
    
    content += f'# {chinese_title}\n\n{english_title}\n\n'
    
    # 剧情简介
    content += f'## 劇情簡介\n\n{movie_data.get("overview", "")}\n\n'
    
    # 评分
    vote_average = movie_data.get('vote_average', 0)
    vote_count = movie_data.get('vote_count', 0)
    content += f'## 評分\n\n⭐ {vote_average}/10 ({vote_count} 票)\n\n'
    
    # 演员列表
    cast = get_cast(movie_data, 8)
    content += '## 主要演員\n\n'
    for actor in cast:
        if actor['name']:
            content += f"- {actor['name']}"
            if actor['character']:
                content += f" ({actor['character']})"
            content += '\n'
    
    # 添加背景图
    backdrop = movie_data.get('backdrop_path', '')
    if backdrop:
        content += f'\n![Backdrop](https://image.tmdb.org/t/p/original{backdrop})\n'
    
    # 完整内容
    full_content = frontmatter + content
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    return chinese_title, english_title

def scrape_now_playing(days=30, page=1):
    """爬取正在上映的電影"""
    url = f'{BASE_URL}/movie/now_playing'
    params = {
        'api_key': TMDB_API_KEY,
        'language': LANGUAGE,
        'page': page
    }
    response = requests.get(url, params=params)
    return response.json()

def main():
    if not TMDB_API_KEY:
        print("❌ 請設置 TMDB_API_KEY 環境變量")
        sys.exit(1)
    
    print("🎬 TMDb 電影爬蟲")
    print("=" * 50)
    
    # 創建目錄
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(POSTER_DIR, exist_ok=True)
    
    # 爬取電影（60部 = 3頁）
    print("\n📡 獲取最近上映的電影...")
    all_movies = []
    for page in range(1, 4):  # 3 pages = 60 movies
        print(f"   📄 第 {page} 頁...")
        page_data = scrape_now_playing(page=page)
        if 'results' in page_data:
            all_movies.extend(page_data['results'])
    
    if not all_movies:
        print("❌ 獲取失敗")
        sys.exit(1)
    
    count = 0
    for movie in all_movies:
        movie_id = movie['id']
        chinese_title = get_chinese_title(movie)
        english_title = get_english_title(movie)
        
        # 獲取詳情
        print(f"\n📥 {chinese_title} ({english_title})")
        details = get_movie_details(movie_id)
        
        # 下載海報
        poster_path = details.get('poster_path', '')
        poster_url = download_poster(poster_path, str(movie_id))
        
        # 生成 Markdown
        filename = f'{movie_id}-{english_title.lower().replace(" ", "-")}.md'
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        cn, en = generate_markdown(details, poster_url, filepath)
        print(f"✅ {cn} ({en})")
        count += 1
        
        # API 限制
        import time
        time.sleep(0.5)
    
    print(f"\n🎉 完成！共生成 {count} 篇文章")
    
    # Git commit
    print("\n📦 Git commit...")
    os.system('git add -A')
    os.system(f'git commit -m "chore: 更新 {count} 部电影"')
    print("✅ 已提交到 GitHub")

if __name__ == '__main__':
    main()
