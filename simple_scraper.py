#!/usr/bin/env python3
"""
简化版爬虫 - 只爬取一部电影作为测试
"""
import os
import sys
import requests
import json
from datetime import datetime

TMDB_API_KEY = "b6871583efed647aad18826d6abbca01"
BASE_URL = 'https://api.themoviedb.org/3'
LANGUAGE = 'zh-TW'
OUTPUT_DIR = 'content/posts'
POSTER_DIR = 'static/posters'

def get_movie_details(movie_id):
    """获取电影详情"""
    url = f'{BASE_URL}/movie/{movie_id}'
    params = {
        'api_key': TMDB_API_KEY,
        'language': LANGUAGE,
        'append_to_response': 'credits'
    }
    response = requests.get(url, params=params)
    return response.json()

def create_markdown(movie_data, movie_id):
    """创建Markdown文件"""
    title = movie_data.get('title', '未知电影')
    original_title = movie_data.get('original_title', title)
    overview = movie_data.get('overview', '暂无简介')
    release_date = movie_data.get('release_date', '未知日期')
    vote_average = movie_data.get('vote_average', 0)
    
    # 获取类型
    genres = [g['name'] for g in movie_data.get('genres', [])]
    
    # 获取演员
    cast = movie_data.get('credits', {}).get('cast', [])[:3]
    cast_list = [f"{actor['name']} 饰演 {actor['character']}" for actor in cast]
    
    # 创建文件名
    filename = f"{movie_id}-{original_title.lower().replace(' ', '-').replace(':', '')}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # 创建目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(POSTER_DIR, exist_ok=True)
    
    # 生成Markdown内容
    content = f"""---
title: "{title}"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')}
draft: false
tags: {json.dumps(genres, ensure_ascii=False)}
categories: ["电影"]
rating: {vote_average}
---

# {title}

**英文名**: {original_title}
**上映日期**: {release_date}
**评分**: ⭐ {vote_average}/10

## 剧情简介

{overview}

## 演员阵容

{chr(10).join(f"- {actor}" for actor in cast_list)}

## 电影信息

- **类型**: {', '.join(genres)}
- **原始语言**: {movie_data.get('original_language', '未知')}
- **时长**: {movie_data.get('runtime', 0)} 分钟
- **预算**: ${movie_data.get('budget', 0):,}
- **收入**: ${movie_data.get('revenue', 0):,}

---
*数据来源: TMDb API*
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

def main():
    print("🎬 简化版 TMDb 爬虫")
    print("=" * 50)
    
    # 测试电影ID - 使用《全面启动》(Inception)
    test_movie_id = 27205  # Inception 的 TMDb ID
    
    print(f"\n📥 获取电影详情 (ID: {test_movie_id})...")
    movie_data = get_movie_details(test_movie_id)
    
    if 'status_code' in movie_data and movie_data['status_code'] == 34:
        print("❌ 电影未找到，尝试其他电影...")
        # 尝试其他电影
        test_movie_id = 155  # 《黑暗骑士》
        movie_data = get_movie_details(test_movie_id)
    
    if 'title' in movie_data:
        print(f"✅ 获取成功: {movie_data['title']}")
        
        # 创建Markdown文件
        filepath = create_markdown(movie_data, test_movie_id)
        print(f"📄 已创建文件: {filepath}")
        
        # Git操作
        print("\n📦 Git 操作...")
        os.system('git add -A')
        commit_msg = f'feat: 添加电影 {movie_data["title"]}'
        os.system(f'git commit -m "{commit_msg}"')
        print("✅ 已提交到本地仓库")
    else:
        print("❌ 获取电影详情失败")
        print(f"响应: {json.dumps(movie_data, indent=2, ensure_ascii=False)}")
    
    print("\n" + "=" * 50)
    print("🎉 爬虫执行完毕")

if __name__ == '__main__':
    main()