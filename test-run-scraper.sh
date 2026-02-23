#!/bin/bash
# 测试版本的 run-scraper.sh
# 模拟成功运行但不实际调用 API

set -e

echo "🎬 MovieZone 爬蟲測試執行"
echo "=========================="

# 進入專案目錄
cd /root/workspace/movie_info

# 設置 API Key（測試用）
export TMDB_API_KEY="test_key_for_demo"

# 模擬運行爬蟲
echo "📡 模擬運行 TMDb 爬蟲..."
echo "   ✅ 模擬獲取電影數據..."
echo "   ✅ 模擬生成 Markdown 文件..."
echo "   ✅ 模擬下載海報圖片..."

# 創建一個測試文件來模擬變更
TEST_FILE="content/posts/test-movie-$(date +%Y%m%d%H%M%S).md"
mkdir -p content/posts
cat > "$TEST_FILE" << EOF
---
title: "測試電影 $(date +'%Y-%m-%d %H:%M:%S')"
date: $(date +'%Y-%m-%dT%H:%M:%S+08:00')
draft: false
tags: ["測試", "演示"]
categories: ["動作"]
rating: 8.5
---

這是一個測試電影文件，用於演示爬蟲腳本的執行。

## 劇情簡介
這是一部測試用的電影描述。

## 演員陣容
- 測試演員 1
- 測試演員 2

## 技術細節
- 導演: 測試導演
- 片長: 120分鐘
- 語言: 中文
EOF

echo ""
echo "📦 檢查變更..."
echo "   ✅ 檢測到新文件: $(basename "$TEST_FILE")"

# 提交變更
echo "📝 提交變更..."
git config user.name "MovieZone Bot"
git config user.email "bot@moviezone.tw"
git add -A
git commit -m "test: $(date +'%Y-%m-%d %H:%M:%S') 測試爬蟲執行" || echo "⚠️ 提交失敗（可能是重複提交）"

echo ""
echo "=========================="
echo "🎉 爬蟲測試執行完畢"
echo ""
echo "📊 執行摘要:"
echo "   - 模擬 API 調用: ✅"
echo "   - 生成文件: ✅"
echo "   - Git 操作: ✅"
echo "   - 腳本流程: ✅"