#!/usr/bin/env python3
"""
TMDB 电影爬虫 - 获取最新电影信息
使用 TMDB API 爬取最新上映的电影详情
"""

import os
import sys
import json
import requests
from datetime import datetime

# 配置
TMDB_API_KEY = "b6871583efed647aad18826d6abbca01"
BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"
BACKDROP_BASE_URL = "https://image.tmdb.org/t/p/original"
LANGUAGE = "zh-CN"

def get_headers():
    return {"api_key": TMDB_API_KEY}

def get_popular_movies(page=1):
    """获取热门电影"""
    url = f"{BASE_URL}/movie/popular"
    params = {
        "api_key": TMDB_API_KEY,
        "language": LANGUAGE,
        "page": page
    }
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()

def get_now_playing_movies():
    """获取正在上映的电影"""
    url = f"{BASE_URL}/movie/now_playing"
    params = {
        "api_key": TMDB_API_KEY,
        "language": LANGUAGE,
        "page": 1
    }
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()

def get_upcoming_movies():
    """获取即将上映的电影"""
    url = f"{BASE_URL}/movie/upcoming"
    params = {
        "api_key": TMDB_API_KEY,
        "language": LANGUAGE,
        "page": 1
    }
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()

def get_movie_details(movie_id):
    """获取电影详情"""
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": LANGUAGE,
        "append_to_response": "credits,images,keywords,recommendations"
    }
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()

def format_movie_card(movie):
    """格式化电影卡片"""
    title = movie.get("title", "未知")
    original_title = movie.get("original_title", "")
    release_date = movie.get("release_date", "未知")
    overview = movie.get("overview", "暂无简介")
    vote_average = movie.get("vote_average", 0)
    vote_count = movie.get("vote_count", 0)
    poster_path = movie.get("poster_path", "")
    backdrop_path = movie.get("backdrop_path", "")
    
    # 类型
    genres = movie.get("genres", [])
    if isinstance(genres, list):
        genre_names = [g.get("name", "") for g in genres if isinstance(g, dict)]
    else:
        genre_names = []
    
    # 演员
    credits = movie.get("credits", {})
    cast = credits.get("cast", [])[:5] if isinstance(credits, dict) else []
    
    # 导演
    directors = [c.get("name", "") for c in credits.get("crew", []) 
                 if c.get("job", "") == "Director"] if isinstance(credits, dict) else []
    
    # 评分
    rating = f"⭐ {vote_average:.1f}/10 ({vote_count} votes)"
    
    # 海报
    poster = f"{POSTER_BASE_URL}{poster_path}" if poster_path else "无"
    
    return {
        "title": title,
        "original_title": original_title,
        "release_date": release_date,
        "overview": overview[:200] + "..." if len(overview) > 200 else overview,
        "rating": rating,
        "genres": genre_names,
        "directors": directors,
        "cast": [c.get("name", "") for c in cast],
        "poster": poster,
        "backdrop": f"{BACKDROP_BASE_URL}{backdrop_path}" if backdrop_path else ""
    }

def print_movie_details(movie_id):
    """打印电影详情"""
    print("=" * 60)
    movie = get_movie_details(movie_id)
    details = format_movie_card(movie)
    
    print(f"\n🎬 {details['title']}")
    if details['original_title'] and details['original_title'] != details['title']:
        print(f"   原名: {details['original_title']}")
    print(f"   📅 {details['release_date']}")
    print(f"   {details['rating']}")
    print(f"   🎭 {', '.join(details['genres']) if details['genres'] else '未知'}")
    if details['directors']:
        print(f"   🎬 导演: {', '.join(details['directors'])}")
    if details['cast']:
        print(f"   👤 演员: {', '.join(details['cast'][:3])}")
    print(f"\n📖 简介:")
    print(f"   {details['overview']}")
    print(f"\n🖼️ 海报: {details['poster']}")
    print("=" * 60)

def list_popular_movies():
    """列出热门电影"""
    print("\n📊 热门电影列表 (Top 20)")
    print("=" * 60)
    
    data = get_popular_movies()
    movies = data.get("results", [])
    
    for i, m in enumerate(movies[:20], 1):
        title = m.get("title", "未知")
        date = m.get("release_date", "未知")[:4] if m.get("release_date") else "未知"
        rating = m.get("vote_average", 0)
        print(f"{i:2d}. {title:<30} ({date}) ⭐ {rating:.1f}")
    
    print("=" * 60)
    return movies

def list_now_playing():
    """列出正在上映的电影"""
    print("\n🎬 正在上映")
    print("=" * 60)
    
    data = get_now_playing_movies()
    movies = data.get("results", [])
    
    for i, m in enumerate(movies[:15], 1):
        title = m.get("title", "未知")
        rating = m.get("vote_average", 0)
        print(f"{i:2d}. {title:<25} ⭐ {rating:.1f}")
    
    print("=" * 60)
    return movies

def list_upcoming():
    """列出即将上映"""
    print("\n📅 即将上映")
    print("=" * 60)
    
    data = get_upcoming_movies()
    movies = data.get("results", [])
    
    for i, m in enumerate(movies[:15], 1):
        title = m.get("title", "未知")
        date = m.get("release_date", "未知")
        print(f"{i:2d}. {title:<25} {date}")
    
    print("=" * 60)
    return movies

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="TMDB 电影爬虫")
    parser.add_argument("--popular", action="store_true", help="热门电影")
    parser.add_argument("--now-playing", action="store_true", help="正在上映")
    parser.add_argument("--upcoming", action="store_true", help="即将上映")
    parser.add_argument("--id", type=int, help="电影 TMDB ID")
    parser.add_argument("--top", type=int, default=10, help="显示数量")
    args = parser.parse_args()
    
    # 默认显示热门
    if args.popular:
        movies = list_popular_movies()
    elif args.now_playing:
        list_now_playing()
    elif args.upcoming:
        list_upcoming()
    elif args.id:
        print_movie_details(args.id)
    else:
        # 显示所有
        list_popular_movies()
        list_now_playing()
        list_upcoming()

if __name__ == "__main__":
    main()
