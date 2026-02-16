#!/usr/bin/env python3
"""
定时爬取即将上映电影并推送到 GitHub
"""

import os
import sys
import json
import requests
import subprocess
from datetime import datetime

# 配置
TMDB_API_KEY = "b6871583efed647aad18826d6abbca01"
REPO_DIR = "/root/.openclaw/workspace/movie_info"
OUTPUT_FILE = os.path.join(REPO_DIR, "content/posts/upcoming-movies.md")

BASE_URL = "https://api.themoviedb.org/3"
LANGUAGE = "zh-CN"

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

def generate_markdown(movies):
    """生成 Markdown"""
    md = f"""---
title: "即将上映电影"
date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
draft: false
---

# 🎬 即将上映电影

> 数据更新时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

| 序号 | 电影 | 原名 | 上映日期 | 评分 |
|:---:|------|------|----------|------:|
"""
    for i, m in enumerate(movies, 1):
        title = m.get("title", "未知")
        original = m.get("original_title", "")
        date = m.get("release_date", "未知")
        rating = m.get("vote_average", 0)
        md += f"| {i} | {title} | {original} | {date} | ⭐ {rating:.1f} |\n"
    
    md += "\n## 电影详情\n\n"
    
    for m in movies[:10]:
        title = m.get("title", "未知")
        original = m.get("original_title", "")
        date = m.get("release_date", "未知")
        rating = m.get("vote_average", 0)
        overview = m.get("overview", "暂无简介")[:150]
        poster = m.get("poster_path", "")
        
        md += f"""### {title}

- **原名**: {original}
- **上映日期**: {date}
- **评分**: ⭐ {rating:.1f}/10
- **简介**: {overview}...

![poster](https://image.tmdb.org/t/p/w500{poster})

---

"""
    
    return md

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
    
    # Commit
    subprocess.run(["git", "commit", "-m", message], capture_output=True)
    
    # Push
    push_result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    if push_result.returncode == 0:
        print("✅ 推送成功")
        return True
    else:
        print(f"❌ 推送失败: {push_result.stderr}")
        return False

def main():
    print(f"⏰ 开始爬取即将上映电影... {datetime.now()}")
    
    # 爬取
    movies = get_upcoming_movies()
    print(f"📊 获取到 {len(movies)} 部电影")
    
    # 生成 Markdown
    md_content = generate_markdown(movies)
    
    # 保存
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"📝 已保存到: {OUTPUT_FILE}")
    
    # Git 提交推送
    message = f"chore: 更新即将上映电影 ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
    success = git_commit_push(message)
    
    if success:
        print("🎉 完成!")
    else:
        print("⚠️ 跳过推送 (无变更或推送失败)")

if __name__ == "__main__":
    main()
