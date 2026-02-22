#!/usr/bin/env python3
"""
定时爬取即将上映电影并推送到 GitHub
生成 Hugo Markdown 格式
"""

import os
import sys
import json
import requests
import subprocess
import urllib.parse
from datetime import datetime

# 配置
TMDB_API_KEY = "b6871583efed647aad18826d6abbca01"
REPO_DIR = "/root/.openclaw/workspace/movie_info"
POSTER_DIR = "static/posters"

BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"
BACKDROP_BASE_URL = "https://image.tmdb.org/t/p/original"
LANGUAGE = "zh-TW"  # 使用繁体中文匹配原格式

def get_upcoming_movies():
    """获取即将上映电影"""
    url = f"{BASE_URL}/movie/upcoming"
    params = {
        "api_key": TMDB_API_KEY,
        "language": LANGUAGE,
        "page": 1
    }
    resp = requests.get(url, params=params, timeout=30)
    return resp.json().get("results", [])[:15]

def get_movie_details(movie_id):
    """获取电影完整详情"""
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": LANGUAGE,
        "append_to_response": "credits"
    }
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()

def slugify(text):
    """生成 slug"""
    # 移除特殊字符，保留中文、英文、数字
    import re
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-').lower()

def download_poster(poster_path, movie_id, save_dir):
    """下载海报"""
    if not poster_path:
        return None
    
    filename = f"{movie_id}.jpg"
    filepath = os.path.join(save_dir, filename)
    
    # 已存在则跳过
    if os.path.exists(filepath):
        return filename
    
    url = f"{POSTER_BASE_URL}{poster_path}"
    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(resp.content)
            return filename
    except Exception as e:
        print(f"❌ 下载海报失败: {e}")
    return None

def format_movie_markdown(movie, save_dir):
    """生成单部电影的 Markdown"""
    movie_id = movie.get("id")
    title = movie.get("title", "未知")
    original_title = movie.get("original_title", title)
    # 使用今天日期，避免 Hugo 默认不发布未来内容
    release_date = datetime.now().strftime("%Y-%m-%d")
    overview = movie.get("overview", "暂无简介")
    rating = movie.get("vote_average", 0)
    rating_count = movie.get("vote_count", 0)
    
    # 获取详情
    details = get_movie_details(movie_id)
    
    # 类型
    genres = details.get("genres", [])
    genre_names = [g.get("name", "") for g in genres]
    categories = json.dumps(genre_names, ensure_ascii=False)
    tags = json.dumps(genre_names, ensure_ascii=False)
    
    # 演职员
    credits = details.get("credits", {})
    cast = credits.get("cast", [])[:8]
    cast_list = []
    for actor in cast:
        name = actor.get("name", "")
        character = actor.get("character", "")
        cast_list.append(f"- {name} ({character})")
    
    # IMDB ID
    imdb_id = details.get("imdb_id", "")
    
    # 海报下载
    poster_path = movie.get("poster_path", "")
    poster_file = download_poster(poster_path, movie_id, save_dir) or f"{movie_id}.jpg"
    
    # 生成 slug
    movie_slug = slugify(original_title)
    filename = f"{movie_id}-{movie_slug}.md"
    filepath = os.path.join(REPO_DIR, "content/posts", filename)
    
    # Markdown 内容
    md = f"""---
title: "{title}"
originalTitle: "{original_title}"
date: {release_date}T00:00:00+08:00
draft: false
Cover: "/posters/{poster_file}"
categories: {categories}
tags: {tags}
rating: {rating:.3f}
ratingCount: {rating_count}
plot: "{overview}"
imdbId: "{imdb_id}"
tmdbId: {movie_id}
---

![Poster](/posters/{poster_file})

# {title}

{original_title}

## 劇情簡介

{overview}

## 評分

⭐ {rating:.3f}/10 ({rating_count} 票)

## 主要演員

"""
    md += "\n".join(cast_list)
    md += f"\n\n![Backdrop]({BACKDROP_BASE_URL}{movie.get('backdrop_path', '')})\n"
    
    return filepath, md

def git_commit_push(message):
    """Git 提交并推送"""
    os.chdir(REPO_DIR)
    
    # Add
    subprocess.run(["git", "add", "-A"], capture_output=True)
    
    # Check status
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if not result.stdout.strip():
        print("没有文件变更")
        return False
    
    # Hugo 测试构建
    print("🔨 测试 Hugo 构建...")
    hugo_result = subprocess.run(
        ["hugo", "-D", "--quiet", "--buildFuture"],
        capture_output=True, text=True, cwd=REPO_DIR
    )
    if hugo_result.returncode != 0:
        print(f"❌ Hugo 构建失败:\n{hugo_result.stderr}")
        # 回滚 git add
        subprocess.run(["git", "reset", "HEAD"], capture_output=True)
        return False
    print("✅ Hugo 构建通过")
    
    # Commit
    subprocess.run(["git", "commit", "-m", message], capture_output=True)
    
    # Push
    push_result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    if push_result.returncode == 0:
        print("✅ 推送成功")
        
        # 生成 commit 日志文件 (在 Hugo 构建后生成)
        log_result = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%H%n%an%n%ae%n%ci%n%s"],
            capture_output=True, text=True, cwd=REPO_DIR
        )
        if log_result.returncode == 0:
            log_lines = log_result.stdout.strip().split('\n')
            commit_info = {
                'hash': log_lines[0] if len(log_lines) > 0 else '',
                'author': log_lines[1] if len(log_lines) > 1 else '',
                'email': log_lines[2] if len(log_lines) > 2 else '',
                'date': log_lines[3] if len(log_lines) > 3 else '',
                'message': log_lines[4] if len(log_lines) > 4 else '',
            }
            
            # 写入日志文件
            log_file = os.path.join(REPO_DIR, "public", "deploy_log.txt")
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            with open(log_file, "w", encoding="utf-8") as f:
                f.write(f"Commit: {commit_info['hash']}\n")
                f.write(f"Author: {commit_info['author']} <{commit_info['email']}>\n")
                f.write(f"Date: {commit_info['date']}\n")
                f.write(f"Message: {commit_info['message']}\n")
            
            # 重新构建 Hugo (会覆盖 public)
            subprocess.run(["hugo", "-D", "--quiet", "--buildFuture"], capture_output=True, cwd=REPO_DIR)
            
            # 再次写入日志文件
            with open(log_file, "w", encoding="utf-8") as f:
                f.write(f"Commit: {commit_info['hash']}\n")
                f.write(f"Author: {commit_info['author']} <{commit_info['email']}>\n")
                f.write(f"Date: {commit_info['date']}\n")
                f.write(f"Message: {commit_info['message']}\n")
            
            # 提交日志文件
            subprocess.run(["git", "add", "public/deploy_log.txt"], capture_output=True, cwd=REPO_DIR)
            subprocess.run(["git", "commit", "-m", "chore: 更新部署日志"], capture_output=True, cwd=REPO_DIR)
            subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True, cwd=REPO_DIR)
        
        return True
    else:
        print(f"❌ 推送失败: {push_result.stderr}")
        return False

def main():
    print(f"⏰ 开始爬取即将上映电影... {datetime.now()}")
    
    # 爬取列表
    movies = get_upcoming_movies()
    print(f"📊 获取到 {len(movies)} 部电影")
    
    save_dir = os.path.join(REPO_DIR, "static/posters")
    os.makedirs(save_dir, exist_ok=True)
    
    count = 0
    for movie in movies:
        try:
            filepath, md_content = format_movie_markdown(movie, save_dir)
            
            # 确保目录存在
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # 保存
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(md_content)
            
            print(f"✅ {movie.get('title')} -> {os.path.basename(filepath)}")
            count += 1
            
        except Exception as e:
            print(f"❌ {movie.get('title')} 失败: {e}")
    
    print(f"📝 已保存 {count} 部电影")
    
    # Git 提交推送
    message = f"chore: 更新即将上映电影 ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
    success = git_commit_push(message)
    
    if success:
        print("🎉 完成!")
    else:
        print("⚠️ 跳过推送 (无变更或推送失败)")

if __name__ == "__main__":
    main()
