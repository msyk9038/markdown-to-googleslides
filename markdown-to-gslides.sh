#!/bin/bash
# マスターの理想的なワークフロー：Markdown → Google Slides
# Usage: ./markdown-to-gslides.sh presentation.md

set -e

# 引数チェック
if [ $# -eq 0 ]; then
    echo "Usage: $0 <markdown-file>"
    echo "Example: $0 presentation.md"
    exit 1
fi

MARKDOWN_FILE="$1"
BASENAME=$(basename "$MARKDOWN_FILE" .md)
PPTX_FILE="${BASENAME}.pptx"

# ファイル存在チェック
if [ ! -f "$MARKDOWN_FILE" ]; then
    echo "❌ Error: $MARKDOWN_FILE not found"
    exit 1
fi

echo "🚀 Starting Markdown → Google Slides workflow..."
echo "   Input: $MARKDOWN_FILE"

# Step 1: Marp CLI でPowerPoint変換
echo "📝 Step 1: Converting Markdown to PowerPoint..."
if ! command -v marp &> /dev/null; then
    echo "❌ Error: Marp CLI not installed. Install with:"
    echo "   npm install -g @marp-team/marp-cli"
    exit 1
fi

marp "$MARKDOWN_FILE" --pptx-editable -o "$PPTX_FILE"
echo "✅ PowerPoint created: $PPTX_FILE"

# Step 2: Google Slides アップロード
echo "☁️  Step 2: Uploading to Google Slides..."
if [ ! -f "upload_to_gslides.py" ]; then
    echo "❌ Error: upload_to_gslides.py not found"
    exit 1
fi

# Google Slidesのファイル名を対話的に設定
read -p "Google Slides file name ($BASENAME): " SLIDE_NAME

if [ -n "$SLIDE_NAME" ]; then
    uv run python upload_to_gslides.py "$PPTX_FILE" --name "$SLIDE_NAME"
else
    uv run python upload_to_gslides.py "$PPTX_FILE"
fi

# Step 3: クリーンアップ（オプション）
read -p "🗑️  Delete local PowerPoint file? (Y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo "📁 Local PowerPoint file kept: $PPTX_FILE"
else
    rm "$PPTX_FILE"
    echo "✅ Local PowerPoint file deleted"
fi

echo "🎉 Workflow complete! Simple is Beautiful."
