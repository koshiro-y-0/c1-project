# WebQ - プロジェクト仕様書

## 概要

**WebQ** は、従来のノーコードツールよりもさらに簡単にウェブサイトを作成できるWebアプリケーションです。
骨組み（テンプレート）は最初から用意されており、ユーザーは画像・テキスト・色を入力するだけでサイトが完成します。

---

## 技術スタック

| カテゴリ | 技術 |
|---------|------|
| バックエンド | Django (Python) |
| フロントエンド | Djangoテンプレート + HTMX + Alpine.js |
| スタイリング | TailwindCSS |
| データベース | SQLite |
| カルーセル | Swiper.js |

---

## 機能要件

### コア機能
- ユーザーごとに複数サイト作成可能
- リアルタイムプレビュー機能
- レスポンシブ対応（モバイル・タブレット・デスクトップ）
- ビジネスライクなデザイン

### URL構造
```
編集ページ:    /sites/{user_id}/{site_id}/
プレビュー:    /preview/{site_id}/
```

---

## セクション構成

セクションは **固定** です（表示/非表示の切り替え不可）。
すべてのサイトは以下の4セクションで構成されます。

### 1. Header + Top

| 要素 | 編集可能 | 説明 |
|------|----------|------|
| タイトル（ロゴ） | ✅ | サイト名を表示 |
| ナビゲーション | ❌ | 固定：「ホーム」「メイン」「詳細」「アクセス」 |
| ナビリンク | ❌ | 各セクション（top, main, sub, access）へのアンカーリンク |
| SNSリンク | ✅ | 表示するSNSとURLを設定 |
| トップ画像 | ✅ | メインビジュアル画像 |

**対応SNS:**
- Instagram
- X (Twitter)
- LINE
- Facebook
- YouTube
- TikTok

### 2. Main（カルーセル）

| 要素 | 編集可能 | 説明 |
|------|----------|------|
| 画像（3枚） | ✅ | カルーセルで表示 |
| タイトル | ✅ | セクションタイトル |
| サブタイトル | ✅ | 補足テキスト |

**カルーセル仕様:**
- 画像枚数: 3枚（固定）
- 自動再生: ON
- 再生間隔: 300ms
- スライド送り時間: 3500ms
- ホバー時: 停止

### 3. Sub（画像 + テキスト）

| 要素 | 編集可能 | 説明 |
|------|----------|------|
| 画像1 | ✅ | 左配置 |
| テキスト1 | ✅ | 画像1の右側 |
| 画像2 | ✅ | 右配置 |
| テキスト2 | ✅ | 画像2の左側 |
| 画像3 | ✅ | 左配置 |
| テキスト3 | ✅ | 画像3の右側 |

**レイアウト:**
```
[画像1] [テキスト1]
[テキスト2] [画像2]
[画像3] [テキスト3]
```

### 4. Access（アクセス情報）

| 要素 | 編集可能 | 説明 |
|------|----------|------|
| セクションタイトル | ✅ | 例：「アクセス」 |
| 住所 | ✅ | 入力した住所でGoogleマップをiframe表示 |
| お問い合わせ | ✅ | 電話番号 |
| 営業時間 | ✅ | 複数時間指定可能 |

**マップ実装:**
- Google Maps Embed API（iframe）を使用
- 住所入力 → iframe埋め込みで対応（APIキー不要）

---

## カスタマイズ機能

### カラー設定
- **各セクションごと** に設定可能
- 背景色: カラーピッカーで自由選択
- 文字色: カラーピッカーで自由選択

### フォント設定
- 各セクションごとにフォントを自由選択
- Google Fonts から選択可能にする

---

## 画像仕様

| 項目 | 仕様 |
|------|------|
| 対応形式 | JPG, PNG, WebP |
| サイズ制限 | なし |
| 保存先 | Django MEDIA_ROOT |

---

## データモデル設計

### User（Django標準）
- Djangoの認証システムを使用

### Site（サイト）
```python
class Site(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)  # サイトタイトル（ロゴ）
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### SectionStyle（セクションスタイル）
```python
class SectionStyle(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    section_name = models.CharField(max_length=20)  # top, main, sub, access
    background_color = models.CharField(max_length=7, default='#FFFFFF')
    text_color = models.CharField(max_length=7, default='#000000')
    font_family = models.CharField(max_length=100, default='Noto Sans JP')
```

### TopSection
```python
class TopSection(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE)
    hero_image = models.ImageField(upload_to='top/')
```

### SNSLink
```python
class SNSLink(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20)  # instagram, x, line, facebook, youtube, tiktok
    url = models.URLField()
    is_active = models.BooleanField(default=True)
```

### MainSection
```python
class MainSection(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    image1 = models.ImageField(upload_to='main/')
    image2 = models.ImageField(upload_to='main/')
    image3 = models.ImageField(upload_to='main/')
```

### SubSection
```python
class SubSection(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='sub/')
    text1 = models.TextField()
    image2 = models.ImageField(upload_to='sub/')
    text2 = models.TextField()
    image3 = models.ImageField(upload_to='sub/')
    text3 = models.TextField()
```

### AccessSection
```python
class AccessSection(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE)
    section_title = models.CharField(max_length=100, default='アクセス')
    address = models.CharField(max_length=300)  # Googleマップ用住所
    phone = models.CharField(max_length=20)
    business_hours = models.JSONField()  # 複数時間指定: [{"day": "月-金", "hours": "9:00-18:00"}, ...]
```

---

## 画面構成

### 1. サイト一覧ページ
- URL: `/sites/{user_id}/`
- ユーザーが作成したサイト一覧を表示
- 新規サイト作成ボタン

### 2. サイト編集ページ
- URL: `/sites/{user_id}/{site_id}/`
- 各セクションの編集フォーム
- リアルタイムプレビュー（HTMX）
- 保存ボタン

### 3. プレビューページ
- URL: `/preview/{site_id}/`
- 実際のサイト表示を確認
- 編集ページへ戻るボタン

---

## ディレクトリ構成

```
webq/
├── manage.py
├── webq/                    # プロジェクト設定
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── sites/                   # メインアプリ
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── migrations/
├── templates/
│   ├── base.html
│   ├── sites/
│   │   ├── list.html        # サイト一覧
│   │   ├── edit.html        # 編集ページ
│   │   └── preview.html     # プレビュー
│   └── components/          # HTMX部分更新用
│       ├── header.html
│       ├── top.html
│       ├── main.html
│       ├── sub.html
│       └── access.html
├── static/
│   ├── css/
│   │   └── styles.css       # TailwindCSS出力
│   ├── js/
│   │   ├── alpine.min.js
│   │   ├── htmx.min.js
│   │   └── swiper.min.js
│   └── images/
└── media/                   # アップロード画像
    ├── top/
    ├── main/
    └── sub/
```

---

## 開発フェーズ

### Phase 1: 基盤構築
- [ ] Djangoプロジェクト作成
- [ ] データモデル実装
- [ ] TailwindCSS設定
- [ ] HTMX + Alpine.js導入

### Phase 2: 編集機能
- [ ] サイト一覧ページ
- [ ] サイト編集ページ（フォーム）
- [ ] 画像アップロード機能
- [ ] カラーピッカー実装

### Phase 3: プレビュー機能
- [ ] プレビューページ
- [ ] リアルタイムプレビュー（HTMX）
- [ ] カルーセル実装（Swiper.js）

### Phase 4: 仕上げ
- [ ] レスポンシブ対応
- [ ] Googleマップiframe埋め込み
- [ ] バリデーション・エラーハンドリング

---

## 将来の拡張機能

| 機能 | 説明 |
|------|------|
| デプロイ機能 | 作成したサイトを公開URL付きでデプロイ |
| アプリデプロイ | WebQ自体を本番環境にデプロイ |
| 認証機能 | ユーザー登録・ログイン・パスワードリセット |
| 英語対応 | i18n対応、UI多言語化 |

---

## コマンドリファレンス

```bash
# 開発サーバー起動
python manage.py runserver

# マイグレーション
python manage.py makemigrations
python manage.py migrate

# 管理者ユーザー作成
python manage.py createsuperuser

# TailwindCSS ビルド（npm使用時）
npm run build:css
```

---

## 注意事項

- 画像形式は **JPG, PNG, WebP** のみ対応
- セクション構成は **固定**（非表示不可）
- Googleマップは **iframe埋め込み**（APIキー不要）
- カルーセルは **3枚固定**
