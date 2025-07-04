---
marp: true
theme: default
paginate: true
---

![bg fit](./pic/background_image.svg)
# Marpサンプル

---

![bg fit](./pic/background_image.svg)
## 自己紹介

- 名前: 太郎
- 職業: エンジニア
- 趣味: プログラミング

---

![bg fit](./pic/background_image.svg)
## 今日の内容

1. Marpの基本
2. 実践的な使い方
3. まとめ

---

![bg fit](./pic/background_image.svg)
## #1.Marpの基本

### Marpとは
- **Marp**: Markdown Presentation Ecosystemの略
- MarkdownでプレゼンテーションスライドをWeb技術で作成
- HTMLとCSSによるカスタマイズが可能

---

![bg fit](./pic/background_image.svg)
### 基本的な書き方

```markdown
---
marp: true
theme: default
---

# タイトル

---

## スライド2

- リスト項目1
- リスト項目2
```

---

![bg fit](./pic/background_image.svg)
### Marpの特徴

- **簡単**: Markdownで書くだけ
- **高速**: リアルタイムプレビュー
- **軽量**: 追加のソフトウェア不要
- **柔軟**: カスタムテーマ対応

---

![bg fit](./pic/background_image.svg)
## #2.実践的な使い方

### 背景画像の設定
```markdown
![bg fit](./pic/background.jpg)
```

### 段階的な表示
```markdown
![bg fit](./pic/background.jpg)
- 最初の項目
- <!-- .element: class="fragment" --> 後で表示
```

---

![bg fit](./pic/background_image.svg)
### テーマのカスタマイズ

```css
/* @theme custom */
section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}
```

---

![bg fit](./pic/background_image.svg)
## #3.まとめ

### Marpの利点
- ✅ Markdownで簡単作成
- ✅ バージョン管理が容易
- ✅ テキストエディタで編集可能
- ✅ 軽量で高速

### 始め方
1. VS Code + Marp拡張機能をインストール
2. `.md`ファイルを作成
3. `marp: true`を設定
4. スライドを書く！

---

![bg fit](./pic/background_image.svg)
# ありがとうございました
