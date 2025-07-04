#!/usr/bin/env python3
"""
PowerPointファイルをGoogle Slidesにアップロード＆変換するCLIツール
Usage: python3 upload_to_gslides.py presentation.pptx [--name "Custom Name"]
"""

import os
import sys
import argparse
import webbrowser
from pathlib import Path

# Google API関連ライブラリ（要インストール）
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    import pickle
except ImportError:
    print("Error: Google API libraries not installed.")
    print("Install with: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    sys.exit(1)

# 必要なスコープ
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/presentations'
]

class GoogleSlidesUploader:
    def __init__(self):
        self.service = None
        self.creds = None
        
    def authenticate(self):
        """Google APIの認証を行う"""
        creds = None
        token_file = 'token.pickle'
        
        # 既存のトークンをロード
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # 認証が無効または期限切れの場合
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # credentials.jsonが必要（Google Cloud Consoleからダウンロード）
                if not os.path.exists('credentials.json'):
                    print("Error: credentials.json not found.")
                    print("Please download from Google Cloud Console:")
                    print("1. Go to https://console.cloud.google.com/")
                    print("2. Create project and enable Drive API & Slides API")
                    print("3. Create OAuth 2.0 credentials")
                    print("4. Download as credentials.json")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            # トークンを保存
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        self.creds = creds
        self.service = build('drive', 'v3', credentials=creds)
        return True
    
    def _check_duplicate_and_handle(self, file_name):
        """既存ファイルの重複チェックと対応"""
        # 同名のGoogle Slidesファイルを検索
        query = f"name='{file_name}' and mimeType='application/vnd.google-apps.presentation' and trashed=false"
        results = self.service.files().list(q=query, fields='files(id,name)').execute()
        existing_files = results.get('files', [])
        
        if not existing_files:
            return file_name  # 重複なし
        
        # 重複があった場合の対処
        print(f"⚠️  A file named '{file_name}' already exists.")
        print("Choose an option:")
        print("1. Overwrite existing file")
        print("2. Create with different name")
        print("3. Cancel upload")
        
        while True:
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == '1':
                # 既存ファイルを削除
                for file in existing_files:
                    self.service.files().delete(fileId=file['id']).execute()
                    print(f"🗑️  Deleted existing file: {file['name']}")
                return file_name
            
            elif choice == '2':
                # 別名を入力
                while True:
                    new_name = input(f"Enter new name (current: {file_name}): ").strip()
                    if new_name:
                        # 新しい名前でも重複チェック
                        return self._check_duplicate_and_handle(new_name)
                    else:
                        print("Please enter a valid name.")
            
            elif choice == '3':
                return None  # キャンセル
            
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
    
    def upload_powerpoint(self, pptx_file, custom_name=None):
        """PowerPointファイルをGoogle Slidesにアップロード＆変換"""
        if not self.service:
            print("Error: Not authenticated. Call authenticate() first.")
            return None
        
        if not os.path.exists(pptx_file):
            print(f"Error: File {pptx_file} not found.")
            return None
        
        print(f"Uploading {pptx_file} to Google Slides...")
        
        # ファイル名の決定（カスタム名が指定されていればそれを使用）
        if custom_name:
            file_name = custom_name
        else:
            file_name = Path(pptx_file).stem
        
        # 既存ファイルの重複チェック
        final_name = self._check_duplicate_and_handle(file_name)
        if final_name is None:
            print("⚠️  Upload cancelled.")
            return None
        
        # Google Slidesとして保存するためのメタデータ
        file_metadata = {
            'name': final_name,
            'mimeType': 'application/vnd.google-apps.presentation'
        }
        
        # PowerPointファイルをアップロード
        media = MediaFileUpload(
            pptx_file,
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
        
        try:
            # ファイルをアップロード＆変換
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink'
            ).execute()
            
            print(f"✅ Success! Google Slides created:")
            print(f"   Name: {file.get('name')}")
            print(f"   ID: {file.get('id')}")
            print(f"   URL: {file.get('webViewLink')}")
            
            return file
            
        except Exception as e:
            print(f"❌ Error uploading file: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(
        description="Upload PowerPoint file to Google Slides"
    )
    parser.add_argument(
        'pptx_file',
        help='PowerPoint file (.pptx) to upload'
    )
    parser.add_argument(
        '--setup',
        action='store_true',
        help='Show setup instructions'
    )
    parser.add_argument(
        '--name',
        type=str,
        help='Custom name for the Google Slides file (optional)'
    )
    
    args = parser.parse_args()
    
    if args.setup:
        print("🔧 Setup Instructions:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create new project or select existing one")
        print("3. Enable APIs: Google Drive API & Google Slides API")
        print("4. Create OAuth 2.0 credentials (Desktop Application)")
        print("5. Download credentials as 'credentials.json'")
        print("6. Install dependencies: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
        return
    
    # PowerPointファイルのバリデーション
    if not args.pptx_file.endswith('.pptx'):
        print("Error: File must be a .pptx file")
        sys.exit(1)
    
    # アップローダーを初期化
    uploader = GoogleSlidesUploader()
    
    # 認証
    if not uploader.authenticate():
        sys.exit(1)
    
    # アップロード実行
    result = uploader.upload_powerpoint(args.pptx_file, args.name)
    
    if result:
        url = result.get('webViewLink')
        print(f"\n🎉 Complete! Opening in browser:")
        print(f"   {url}")
        
        # ブラウザで自動的に開く
        try:
            webbrowser.open(url)
            print("✅ Browser opened successfully")
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print("Please open the URL manually")
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()