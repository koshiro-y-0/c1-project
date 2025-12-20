# WebQ - かんたんウェブサイト作成ツール

WebQは、テンプレートベースで簡単にウェブサイトを作成できるWebアプリケーションです。
画像・テキスト・色を入力するだけで、ビジネスライクなウェブサイトが完成します。

## 機能

- **サイト管理**: ユーザーごとに複数サイト作成可能
- **セクション編集**: Header/Top、Main（カルーセル）、Sub、Accessの4セクション
- **スタイル設定**: セクションごとに背景色・文字色・フォントを設定
- **リアルタイムプレビュー**: 編集内容を即座に確認
- **レスポンシブ対応**: モバイル・タブレット・デスクトップに対応
- **SNSリンク**: Instagram、X、LINE、Facebook、YouTube、TikTok対応
- **Googleマップ連携**: 住所入力で自動的にマップを表示

## 技術スタック

| カテゴリ | 技術 |
|---------|------|
| バックエンド | Django 5.x (Python) |
| フロントエンド | Django Templates + HTMX + Alpine.js |
| スタイリング | TailwindCSS |
| データベース | SQLite |
| カルーセル | Swiper.js |

## セットアップ手順

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd c1-project
```

### 2. Python仮想環境のセットアップ

```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
# Linux/Mac:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 依存パッケージのインストール
pip install -r requirements.txt
```

### 3. Node.js依存のインストール（TailwindCSS用）

```bash
npm install
```

### 4. データベースのセットアップ

```bash
# マイグレーション実行
python manage.py migrate

# 管理者ユーザー作成
python manage.py createsuperuser
```

### 5. 開発サーバーの起動

```bash
# TailwindCSSのビルド（別ターミナル）
npm run build:css

# または監視モード
npm run dev

# Djangoサーバー起動
python manage.py runserver
```

アプリケーションは http://127.0.0.1:8000 でアクセスできます。

## URL構成

| URL | 説明 |
|-----|------|
| `/sites/<user_id>/` | サイト一覧 |
| `/sites/<user_id>/create/` | サイト新規作成 |
| `/sites/<user_id>/<site_id>/` | サイト編集 |
| `/preview/<site_id>/` | プレビュー表示 |
| `/admin/` | 管理画面 |

## 使い方

### 1. サイト一覧

サイト一覧ページ（`/sites/<user_id>/`）では、作成したサイトの一覧が表示されます。
「新規サイト作成」ボタンをクリックして、新しいサイトを作成できます。

### 2. サイト編集

編集ページでは、以下のタブで各セクションを編集できます：

- **基本設定**: サイトタイトル
- **トップ**: ヒーロー画像、スタイル設定
- **メイン**: カルーセル画像（3枚）、タイトル、サブタイトル
- **サブ**: 画像とテキストの交互レイアウト（3セット）
- **アクセス**: 住所（Googleマップ）、電話番号、営業時間
- **SNS**: 各SNSプラットフォームのURL

各セクションで「保存」ボタンをクリックすると変更が保存されます。

### 3. プレビュー

「プレビュー」ボタンをクリックすると、実際のサイト表示を確認できます。

## 画像仕様

| 項目 | 仕様 |
|------|------|
| 対応形式 | JPG, PNG, WebP |
| 保存先 | `media/` ディレクトリ |

## ディレクトリ構成

```
c1-project/
├── manage.py
├── webq/                    # プロジェクト設定
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── sites/                   # メインアプリ
│   ├── models.py           # データモデル
│   ├── views.py            # ビュー
│   ├── urls.py             # URL設定
│   ├── forms.py            # フォーム
│   ├── admin.py            # 管理画面
│   └── tests.py            # テスト
├── templates/
│   ├── base.html
│   ├── sites/              # サイト関連テンプレート
│   └── components/         # コンポーネント
├── static/
│   └── css/
│       ├── input.css       # TailwindCSS入力
│       └── styles.css      # TailwindCSSビルド出力
└── media/                   # アップロード画像
```

## テスト

```bash
# テスト実行
python manage.py test sites

# 詳細出力
python manage.py test sites -v 2
```

## コマンドリファレンス

```bash
# 開発サーバー起動
python manage.py runserver

# マイグレーション作成
python manage.py makemigrations

# マイグレーション実行
python manage.py migrate

# 静的ファイル収集（本番用）
python manage.py collectstatic

# TailwindCSS ビルド
npm run build:css

# TailwindCSS 監視モード
npm run dev
```

## ライセンス

MIT License
