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
- [ ] Site モデル作成
  - [ ] user (ForeignKey)
  - [ ] title (CharField)
  - [ ] created_at, updated_at

- [ ] SectionStyle モデル作成
  - [ ] site (ForeignKey)
  - [ ] section_name (CharField)
  - [ ] background_color (CharField)
  - [ ] text_color (CharField)
  - [ ] font_family (CharField)

- [ ] TopSection モデル作成
  - [ ] site (OneToOneField)
  - [ ] hero_image (ImageField)

- [ ] SNSLink モデル作成
  - [ ] site (ForeignKey)
  - [ ] platform (CharField)
  - [ ] url (URLField)
  - [ ] is_active (BooleanField)

- [ ] MainSection モデル作成
  - [ ] site (OneToOneField)
  - [ ] title, subtitle
  - [ ] image1, image2, image3

- [ ] SubSection モデル作成
  - [ ] site (OneToOneField)
  - [ ] image1, text1
  - [ ] image2, text2
  - [ ] image3, text3

- [ ] AccessSection モデル作成
  - [ ] site (OneToOneField)
  - [ ] section_title
  - [ ] address
  - [ ] phone
  - [ ] business_hours (JSONField)

### 2.2 マイグレーション
- [ ] マイグレーションファイル作成
- [ ] マイグレーション実行
- [ ] 管理者ユーザー作成

### 2.3 Django Admin設定
- [ ] 各モデルをadmin.pyに登録
- [ ] 管理画面でのデータ確認

---

## Phase 3: URL・ビュー基盤

### 3.1 URL設定
- [ ] webq/urls.py にsitesアプリのURL include
- [ ] sites/urls.py 作成
  - [ ] サイト一覧: `sites/<int:user_id>/`
  - [ ] サイト編集: `sites/<int:user_id>/<int:site_id>/`
  - [ ] プレビュー: `preview/<int:site_id>/`
  - [ ] サイト新規作成: `sites/<int:user_id>/create/`

### 3.2 基本ビュー作成
- [ ] site_list ビュー（サイト一覧）
- [ ] site_create ビュー（新規作成）
- [ ] site_edit ビュー（編集）
- [ ] site_preview ビュー（プレビュー）

---

## Phase 4: テンプレート・フロントエンド

### 4.1 ベーステンプレート
- [ ] base.html 作成
  - [ ] HTML5構造
  - [ ] TailwindCSS読み込み
  - [ ] HTMX読み込み
  - [ ] Alpine.js読み込み
  - [ ] Swiper.js読み込み（必要なページのみ）

### 4.2 サイト一覧ページ
- [ ] templates/sites/list.html 作成
- [ ] サイトカード表示
- [ ] 新規作成ボタン
- [ ] レスポンシブレイアウト

### 4.3 サイト編集ページ
- [ ] templates/sites/edit.html 作成
- [ ] セクションごとのフォーム
  - [ ] Header + Top フォーム
  - [ ] Main フォーム
  - [ ] Sub フォーム
  - [ ] Access フォーム
- [ ] カラーピッカー実装
- [ ] フォント選択実装
- [ ] 画像アップロードUI
- [ ] プレビューボタン
- [ ] 保存ボタン

### 4.4 プレビューページ
- [ ] templates/sites/preview.html 作成
- [ ] 実際のサイト表示レイアウト
- [ ] 編集ページへ戻るボタン

---

## Phase 5: コンポーネント実装

### 5.1 Header + Top コンポーネント
- [ ] templates/components/header.html
- [ ] ロゴ表示
- [ ] ナビゲーションメニュー
- [ ] SNSアイコンリンク
- [ ] アンカーリンク設定（#top, #main, #sub, #access）

- [ ] templates/components/top.html
- [ ] ヒーロー画像表示
- [ ] レスポンシブ対応

### 5.2 Main コンポーネント
- [ ] templates/components/main.html
- [ ] Swiper.jsカルーセル実装
  - [ ] 3枚の画像スライド
  - [ ] 自動再生（300ms間隔）
  - [ ] スライド送り（3500ms）
  - [ ] ホバー停止
  - [ ] ナビゲーションボタン
- [ ] タイトル・サブタイトル表示

### 5.3 Sub コンポーネント
- [ ] templates/components/sub.html
- [ ] 画像とテキストの交互配置レイアウト
  - [ ] 画像1（左）+ テキスト1（右）
  - [ ] テキスト2（左）+ 画像2（右）
  - [ ] 画像3（左）+ テキスト3（右）
- [ ] レスポンシブ対応（モバイルでは縦積み）

### 5.4 Access コンポーネント
- [ ] templates/components/access.html
- [ ] Googleマップ iframe埋め込み
  - [ ] 住所からiframe URL生成
- [ ] 電話番号表示
- [ ] 営業時間表示（複数対応）

---

## Phase 6: フォーム・HTMX実装

### 6.1 フォームクラス作成
- [ ] sites/forms.py 作成
- [ ] SiteForm（基本情報）
- [ ] TopSectionForm
- [ ] SNSLinkFormSet（複数SNS対応）
- [ ] MainSectionForm
- [ ] SubSectionForm
- [ ] AccessSectionForm
- [ ] SectionStyleForm

### 6.2 画像アップロード
- [ ] 画像バリデーション（JPG, PNG, WebP）
- [ ] 画像保存処理
- [ ] 画像プレビュー表示

### 6.3 HTMXリアルタイムプレビュー
- [ ] 入力時の部分更新エンドポイント作成
- [ ] hx-trigger="input" 設定
- [ ] hx-target でプレビューエリア更新
- [ ] debounce設定（入力遅延）

### 6.4 フォーム保存処理
- [ ] 各セクションの保存ビュー
- [ ] バリデーションエラー表示
- [ ] 保存成功メッセージ

---

## Phase 7: スタイリング

### 7.1 TailwindCSS カスタマイズ
- [ ] tailwind.config.js カスタマイズ
- [ ] カラーパレット定義
- [ ] フォント設定

### 7.2 共通スタイル
- [ ] ボタンスタイル
- [ ] フォームスタイル
- [ ] カードスタイル
- [ ] カラーピッカースタイル

### 7.3 レスポンシブ対応
- [ ] モバイル（~640px）
- [ ] タブレット（641px~1024px）
- [ ] デスクトップ（1025px~）
- [ ] 各ブレークポイントでのレイアウト確認

### 7.4 ビジネスライクデザイン
- [ ] 適切な余白設定
- [ ] フォントサイズ調整
- [ ] カラーコントラスト確認

---

## Phase 8: 機能完成・テスト

### 8.1 統合テスト
- [ ] サイト新規作成フロー
- [ ] 各セクション編集フロー
- [ ] 画像アップロードフロー
- [ ] プレビュー表示確認
- [ ] レスポンシブ表示確認

### 8.2 エッジケース対応
- [ ] 空のフィールド処理
- [ ] 不正な画像形式エラー
- [ ] 長いテキスト入力

### 8.3 ブラウザテスト
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] モバイルブラウザ

---

## Phase 9: 仕上げ

### 9.1 コード整理
- [ ] 不要なコード削除
- [ ] コメント追加
- [ ] 命名規則統一

### 9.2 ドキュメント
- [ ] README.md 更新
- [ ] セットアップ手順記載
- [ ] 使い方説明

### 9.3 セキュリティ確認
- [ ] CSRF対策確認
- [ ] 画像アップロードセキュリティ
- [ ] XSS対策

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
| Phase 2 | 23 | 0 | 0% |
| Phase 3 | 8 | 0 | 0% |
| Phase 4 | 17 | 0 | 0% |
| Phase 5 | 18 | 0 | 0% |
| Phase 6 | 14 | 0 | 0% |
| Phase 7 | 12 | 0 | 0% |
| Phase 8 | 10 | 0 | 0% |
| Phase 9 | 9 | 0 | 0% |
| **合計** | **136** | **25** | **18%** |

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
