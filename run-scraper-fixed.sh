#!/bin/bash
# 修复版的 run-scraper.sh
# 使用有效的 API Key 和修复的路径

set -e

echo "🎬 MovieZone 爬蟲開始執行"
echo "=========================="

# 進入專案目錄
cd /root/workspace/movie_info

# 設置 API Key
export TMDB_API_KEY="b6871583efed647aad18826d6abbca01"

# 運行爬蟲
echo "📡 運行 TMDb 爬蟲..."
python3 simple_scraper.py

# 檢查是否有變更
echo ""
echo "📦 檢查變更..."
if git diff --stat HEAD~1 | grep -q "0 files changed"; then
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

# 顯示生成的檔案
echo ""
echo "📁 生成的檔案:"
find content/posts -name "*.md" -newer /tmp/start_time 2>/dev/null || find content/posts -name "*.md" | tail -5