# markdown-to-googleslides

Markdown作成 → Google Slidesにアップロードするワークフローを実現するツール群

## Description

MarkdownからGoogle Slidesプレゼンテーションを効率的に作成するためのCLIツールセットです。

## Features

- ✅ **Marp CLI** による高品質なPowerPoint変換
- ✅ **Google Drive API** 連携での自動アップロード
- ✅ **ワンコマンド** でGoogle Slides作成

## Setup

### 1. 依存関係のインストール

```bash
# Node.js パッケージ
npm install -g @marp-team/marp-cli

# Python ライブラリ（uvを使用）
uv sync
```

**重要：** `--pptx-editable` オプションを使用する場合は LibreOffice 24.8.7.2 を推奨します。25.x系では互換性問題が発生します。

LibreOffice 24.8.7.2 のインストール手順（macOS）：
1. 現在のLibreOfficeをアンインストール（必要な場合）
2. [LibreOffice 24.8.7](https://www.libreoffice.org/donate/dl/mac-aarch64/24.8.7/ja/LibreOffice_24.8.7_MacOS_aarch64.dmg) から直接ダウンロード（Apple Silicon Mac用）

### 2. Google Cloud Console設定

**手順:**
1. [Google Cloud Console](https://console.cloud.google.com/) でプロジェクト作成
2. Google Drive API & Google Slides API を有効化
3. OAuth 2.0 認証情報（デスクトップアプリケーション）を作成
4. `credentials.json` としてダウンロードしてプロジェクトルートに配置

### 3. スクリプトに実行権限を付与

```bash
chmod +x markdown-to-gslides.sh
chmod +x upload_to_gslides.py
```

## Usage

### 基本的な使用方法

```bash
# 1. Markdown編集
vim presentation.md

# 2. ワンコマンドで Google Slides 作成
./markdown-to-gslides.sh presentation.md

# 3. ブラウザで微調整
# → 自動でブラウザが開きます
```

### Markdownファイルの書き方

```markdown
---
marp: true
theme: default
paginate: true
---

# タイトルスライド

プレゼンテーションの内容

---

## セクション1

- ポイント1
- ポイント2
- ポイント3

---

## まとめ

**Simple is Beautiful.**
```

### 個別コマンド

```bash
# PowerPointへ変換のみしたい
marp presentation.md --pptx -o presentation.pptx #編集不可能
marp presentation.md --pptx-editable -o presentation.pptx #編集可能（実験的機能）

# Google Slidesアップロードのみ
uv run python upload_to_gslides.py presentation.pptx

# カスタム名でアップロード
uv run python upload_to_gslides.py presentation.pptx --name "私のプレゼンテーション"
```

## ファイル構成

```
markdown-to-googleslides/
├── README.md                    # このファイル
├── pyproject.toml              # uvプロジェクト設定
├── .venv/                      # Python仮想環境
├── markdown-to-gslides.sh      # メインワークフロースクリプト
├── upload_to_gslides.py        # Google Slides アップロードスクリプト
├── sample-marp.md              # サンプルMarkdownファイル
├── credentials.json            # Google API認証情報（要設定）
└── token.pickle               # 認証トークン（自動生成）
```

## Topics

- markdown
- google-slides
- marp

## License

MIT License
