# WebQ 開発実行計画 - TODOリスト

## 概要

このドキュメントはWebQアプリケーションを構築するための詳細な実行計画です。
各フェーズのタスクを順番に実行することで、アプリケーションを完成させます。

---

## Phase 0: 環境構築

### 0.1 Python環境
- [x] Python仮想環境の作成 (`python -m venv venv`)
- [x] 仮想環境の有効化
- [x] pip のアップグレード

### 0.2 パッケージインストール
- [x] Django インストール
- [x] Pillow インストール（画像処理用）
- [x] django-htmx インストール
- [x] requirements.txt 作成

### 0.3 Node.js環境（TailwindCSS用）
- [x] package.json 作成
- [x] TailwindCSS インストール
- [x] postcss, autoprefixer インストール
- [x] tailwind.config.js 作成
- [x] ビルドスクリプト設定

---

## Phase 1: Djangoプロジェクト基盤

### 1.1 プロジェクト作成
- [x] Djangoプロジェクト作成 (`django-admin startproject webq .`)
- [x] sitesアプリ作成 (`python manage.py startapp sites`)
- [x] settings.py の基本設定
  - [x] INSTALLED_APPS に sites 追加
  - [x] TEMPLATES 設定
  - [x] STATIC_URL, STATICFILES_DIRS 設定
  - [x] MEDIA_URL, MEDIA_ROOT 設定
  - [x] 言語・タイムゾーン設定（ja, Asia/Tokyo）

### 1.2 ディレクトリ構造作成
- [x] templates/ ディレクトリ作成
- [x] templates/sites/ ディレクトリ作成
- [x] templates/components/ ディレクトリ作成
- [x] static/ ディレクトリ作成
- [x] static/css/ ディレクトリ作成
- [x] static/js/ ディレクトリ作成
- [x] media/ ディレクトリ作成

### 1.3 静的ファイル準備
- [x] HTMX ダウンロード/CDN設定
- [x] Alpine.js ダウンロード/CDN設定
- [x] Swiper.js ダウンロード/CDN設定
- [x] TailwindCSS 入力ファイル作成 (input.css)
- [x] TailwindCSS ビルド確認

---

## Phase 2: データモデル実装

### 2.1 モデル定義
- [x] Site モデル作成
  - [x] user (ForeignKey)
  - [x] title (CharField)
  - [x] created_at, updated_at

- [x] SectionStyle モデル作成
  - [x] site (ForeignKey)
  - [x] section_name (CharField)
  - [x] background_color (CharField)
  - [x] text_color (CharField)
  - [x] font_family (CharField)

- [x] TopSection モデル作成
  - [x] site (OneToOneField)
  - [x] hero_image (ImageField)

- [x] SNSLink モデル作成
  - [x] site (ForeignKey)
  - [x] platform (CharField)
  - [x] url (URLField)
  - [x] is_active (BooleanField)

- [x] MainSection モデル作成
  - [x] site (OneToOneField)
  - [x] title, subtitle
  - [x] image1, image2, image3

- [x] SubSection モデル作成
  - [x] site (OneToOneField)
  - [x] image1, text1
  - [x] image2, text2
  - [x] image3, text3

- [x] AccessSection モデル作成
  - [x] site (OneToOneField)
  - [x] section_title
  - [x] address
  - [x] phone
  - [x] business_hours (JSONField)

### 2.2 マイグレーション
- [x] マイグレーションファイル作成
- [x] マイグレーション実行
- [x] 管理者ユーザー作成

### 2.3 Django Admin設定
- [x] 各モデルをadmin.pyに登録
- [x] 管理画面でのデータ確認

---

## Phase 3: URL・ビュー基盤

### 3.1 URL設定
- [x] webq/urls.py にsitesアプリのURL include
- [x] sites/urls.py 作成
  - [x] サイト一覧: `sites/<int:user_id>/`
  - [x] サイト編集: `sites/<int:user_id>/<int:site_id>/`
  - [x] プレビュー: `preview/<int:site_id>/`
  - [x] サイト新規作成: `sites/<int:user_id>/create/`

### 3.2 基本ビュー作成
- [x] site_list ビュー（サイト一覧）
- [x] site_create ビュー（新規作成）
- [x] site_edit ビュー（編集）
- [x] site_preview ビュー（プレビュー）

---

## Phase 4: テンプレート・フロントエンド

### 4.1 ベーステンプレート
- [x] base.html 作成
  - [x] HTML5構造
  - [x] TailwindCSS読み込み
  - [x] HTMX読み込み
  - [x] Alpine.js読み込み
  - [x] Swiper.js読み込み（必要なページのみ）

### 4.2 サイト一覧ページ
- [x] templates/sites/list.html 作成
- [x] サイトカード表示
- [x] 新規作成ボタン
- [x] レスポンシブレイアウト

### 4.3 サイト編集ページ
- [x] templates/sites/edit.html 作成
- [x] セクションごとのフォーム
  - [x] Header + Top フォーム
  - [x] Main フォーム
  - [x] Sub フォーム
  - [x] Access フォーム
- [x] カラーピッカー実装
- [x] フォント選択実装
- [x] 画像アップロードUI
- [x] プレビューボタン
- [x] 保存ボタン

### 4.4 プレビューページ
- [x] templates/sites/preview.html 作成
- [x] 実際のサイト表示レイアウト
- [x] 編集ページへ戻るボタン

---

## Phase 5: コンポーネント実装

### 5.1 Header + Top コンポーネント
- [x] templates/components/header.html
- [x] ロゴ表示
- [x] ナビゲーションメニュー
- [x] SNSアイコンリンク
- [x] アンカーリンク設定（#top, #main, #sub, #access）

- [x] templates/components/top.html
- [x] ヒーロー画像表示
- [x] レスポンシブ対応

### 5.2 Main コンポーネント
- [x] templates/components/main.html
- [x] Swiper.jsカルーセル実装
  - [x] 3枚の画像スライド
  - [x] 自動再生（300ms間隔）
  - [x] スライド送り（3500ms）
  - [x] ホバー停止
  - [x] ナビゲーションボタン
- [x] タイトル・サブタイトル表示

### 5.3 Sub コンポーネント
- [x] templates/components/sub.html
- [x] 画像とテキストの交互配置レイアウト
  - [x] 画像1（左）+ テキスト1（右）
  - [x] テキスト2（左）+ 画像2（右）
  - [x] 画像3（左）+ テキスト3（右）
- [x] レスポンシブ対応（モバイルでは縦積み）

### 5.4 Access コンポーネント
- [x] templates/components/access.html
- [x] Googleマップ iframe埋め込み
  - [x] 住所からiframe URL生成
- [x] 電話番号表示
- [x] 営業時間表示（複数対応）

---

## Phase 6: フォーム・HTMX実装

### 6.1 フォームクラス作成
- [x] sites/forms.py 作成
- [x] SiteForm（基本情報）
- [x] TopSectionForm
- [x] SNSLinkFormSet（複数SNS対応）
- [x] MainSectionForm
- [x] SubSectionForm
- [x] AccessSectionForm
- [x] SectionStyleForm

### 6.2 画像アップロード
- [x] 画像バリデーション（JPG, PNG, WebP）
- [x] 画像保存処理
- [x] 画像プレビュー表示

### 6.3 HTMXリアルタイムプレビュー
- [x] 入力時の部分更新エンドポイント作成
- [x] hx-trigger="input" 設定
- [x] hx-target でプレビューエリア更新
- [x] debounce設定（入力遅延）

### 6.4 フォーム保存処理
- [x] 各セクションの保存ビュー
- [x] バリデーションエラー表示
- [x] 保存成功メッセージ

---

## Phase 7: スタイリング

### 7.1 TailwindCSS カスタマイズ
- [x] tailwind.config.js カスタマイズ
- [x] カラーパレット定義
- [x] フォント設定

### 7.2 共通スタイル
- [x] ボタンスタイル
- [x] フォームスタイル
- [x] カードスタイル
- [x] カラーピッカースタイル

### 7.3 レスポンシブ対応
- [x] モバイル（~640px）
- [x] タブレット（641px~1024px）
- [x] デスクトップ（1025px~）
- [x] 各ブレークポイントでのレイアウト確認

### 7.4 ビジネスライクデザイン
- [x] 適切な余白設定
- [x] フォントサイズ調整
- [x] カラーコントラスト確認

---

## Phase 8: 機能完成・テスト

### 8.1 統合テスト
- [x] サイト新規作成フロー
- [x] 各セクション編集フロー
- [x] 画像アップロードフロー
- [x] プレビュー表示確認
- [x] レスポンシブ表示確認

### 8.2 エッジケース対応
- [x] 空のフィールド処理
- [x] 不正な画像形式エラー
- [x] 長いテキスト入力

### 8.3 ブラウザテスト
- [x] Chrome
- [x] Firefox
- [x] Safari
- [x] モバイルブラウザ

---

## Phase 9: 仕上げ

### 9.1 コード整理
- [x] 不要なコード削除
- [x] コメント追加
- [x] 命名規則統一

### 9.2 ドキュメント
- [x] README.md 更新
- [x] セットアップ手順記載
- [x] 使い方説明

### 9.3 セキュリティ確認
- [x] CSRF対策確認
- [x] 画像アップロードセキュリティ
- [x] XSS対策

---

## 将来フェーズ（拡張機能）

### Future 1: 認証機能
- [ ] ユーザー登録
- [ ] ログイン/ログアウト
- [ ] パスワードリセット
- [ ] アクセス制御

### Future 2: デプロイ
- [ ] 本番用設定
- [ ] 静的ファイル収集
- [ ] デプロイ先選定
- [ ] デプロイ実行

### Future 3: 英語対応
- [ ] i18n設定
- [ ] 翻訳ファイル作成
- [ ] 言語切り替えUI

---

## 進捗サマリー

| フェーズ | タスク数 | 完了 | 進捗 |
|---------|---------|------|------|
| Phase 0 | 9 | 9 | 100% |
| Phase 1 | 16 | 16 | 100% |
| Phase 2 | 23 | 23 | 100% |
| Phase 3 | 8 | 8 | 100% |
| Phase 4 | 17 | 17 | 100% |
| Phase 5 | 18 | 18 | 100% |
| Phase 6 | 14 | 14 | 100% |
| Phase 7 | 12 | 12 | 100% |
| Phase 8 | 10 | 10 | 100% |
| Phase 9 | 9 | 9 | 100% |
| **合計** | **136** | **136** | **100%** |

---

## 実行順序の注意

1. **Phase 0 → 1 → 2** は順番に実行（依存関係あり）
2. **Phase 3 → 4 → 5 → 6** は順番に実行（依存関係あり）
3. **Phase 7** はPhase 5, 6と並行して進めてもOK
4. **Phase 8** はすべての機能実装後
5. **Phase 9** は最後に実行

---

## 推定作業ボリューム

| フェーズ | 内容 | ボリューム |
|---------|------|-----------|
| Phase 0 | 環境構築 | 小 |
| Phase 1 | Django基盤 | 小 |
| Phase 2 | データモデル | 中 |
| Phase 3 | URL・ビュー | 小 |
| Phase 4 | テンプレート | 中 |
| Phase 5 | コンポーネント | 大 |
| Phase 6 | フォーム・HTMX | 大 |
| Phase 7 | スタイリング | 中 |
| Phase 8 | テスト | 中 |
| Phase 9 | 仕上げ | 小 |
