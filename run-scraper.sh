#!/bin/bash
# MovieZone 爬蟲自動執行腳本
# Cron: 0 8 * * *
# 用法: ./run-scraper.sh

set -e

echo "🎬 MovieZone 爬蟲開始執行"
echo "=========================="

# 進入專案目錄
cd /root/workspace/movie_info

# 設置 API Key
export TMDB_API_KEY="API_KEY_PLACEHOLDER"

# 運行爬蟲
echo "📡 運行 TMDb 爬蟲..."
python3 scripts/scrape-tmdb.py

# 檢查是否有變更
echo ""
echo "📦 檢查變更..."
if git diff --stat | grep -q "0 files changed"; then
    echo "✅ 沒有新電影，跳過提交"
else
    # 提交變更
    echo "📝 提交變更..."
    git config user.name "MovieZone Bot"
    git config user.email "bot@moviezone.tw"
    git add -A
    git commit -m "chore: $(date +'%Y-%m-%d') 更新電影"

    # 推送到 GitHub
    echo "🚀 推送到 GitHub..."
    git push origin main || echo "⚠️ 推送失敗，可能需要手動處理"

    echo ""
    echo "✅ 完成！Vercel 將自動部署"
fi

echo ""
echo "=========================="
echo "🎉 爬蟲執行完畢"
