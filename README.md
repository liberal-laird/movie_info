# MovieZone 電影資訊網站

雙語電影資訊網站，使用 Hugo + Vercel 構建。

## 項目結構

```
movie-site/
├── content/
│   └── movies/              # 電影文章 (Markdown)
├── static/
│   └── posters/             # 海報圖片
├── scripts/
│   └── scrape-tmdb.py       # TMDb 爬蟲腳本
├── layouts/                 # Hugo 模板
├── hugo.toml               # Hugo 配置
├── vercel.json             # Vercel 配置
└── .github/workflows/
    └── daily-update.yml    # 每日自動更新
```

## 快速開始

### 1. 本地開發

```bash
# 安裝 Hugo
brew install hugo  # macOS
# 或
apt-get install hugo  # Linux

# 啟動本地伺服器
hugo server
```

### 2. 配置 TMDb API

設置環境變量：
```bash
export TMDB_API_KEY="your_api_key"
```

獲取 API Key：https://www.themoviedb.org/settings/api

### 3. 手動運行爬蟲

```bash
python scripts/scrape-tmdb.py
```

## 部署

### Vercel

1. 連接 GitHub 倉庫到 Vercel
2. 設置環境變量：
   - `TMDB_API_KEY`
3. 自動部署完成！

### GitHub Actions

每日自動任務：
1. 爬取 TMDb 電影
2. 生成 Markdown 文章
3. Git commit + push
4. Vercel 自動部署

## 環境變量

| 變量 | 說明 |
|------|------|
| `TMDB_API_KEY` | TMDb API Key |
| `OUTPUT_DIR` | 輸出目錄 (預設: content/movies) |
| `POSTER_DIR` | 海報目錄 (預設: static/posters) |

## 技術棧

- **框架**: Hugo
- **托管**: Vercel
- **數據源**: TMDb API
- **自動化**: GitHub Actions
- **爬蟲**: Python

## License

MIT.
