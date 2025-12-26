# 修正履歴

## 2025-12-23: ルートURL Page Not Found 修正

### 問題
- ルートURL（`http://localhost:8000/`）にアクセスすると「Page not found」エラーが発生

### 原因
- ルートURL（`/`）に対応するビューが設定されていなかった

### 修正内容
**ファイル**: `webq/urls.py`

```python
# 追加したインポート
from django.shortcuts import redirect

# 追加したビュー関数
def home_redirect(request):
    """ルートURLからサイト一覧へリダイレクト"""
    return redirect('sites:site_list', user_id=1)

# urlpatternsに追加
urlpatterns = [
    path("", home_redirect, name="home"),  # この行を追加
    path("admin/", admin.site.urls),
    path("sites/", include("sites.urls")),
]
```

### 動作
- `http://localhost:8000/` にアクセスすると自動的に `http://localhost:8000/sites/1/` にリダイレクトされる

---

## 2025-12-26: 画像サイズ調整・フォント拡張・プレビュー全幅対応

### 1. 画像サイズ調整機能を追加

#### 問題
- 各セクションで画像を入れた際に、画像のサイズが合わないことが多い

#### 修正内容
**ファイル**: `sites/models.py`

各セクション（TopSection, MainSection, SubSection）に以下のフィールドを追加：
- `image_fit`: 画像表示モード（cover/contain/fill）
- `image_height`: 画像高さ（px）

```python
# TopSection
hero_image_fit = models.CharField('画像表示モード', max_length=20, choices=IMAGE_FIT_CHOICES, default='cover')
hero_image_height = models.IntegerField('画像高さ(px)', default=500)

# MainSection, SubSection
image_fit = models.CharField('画像表示モード', max_length=20, choices=IMAGE_FIT_CHOICES, default='cover')
image_height = models.IntegerField('画像高さ(px)', default=400)  # SubSectionは256
```

**ファイル**: `sites/forms.py`

フォームにフィールドを追加してUIから設定可能に

**ファイル**: `templates/sites/preview.html`

画像のスタイルを動的に適用：
```html
<img style="height: {{ main_section.image_height }}px; object-fit: {{ main_section.image_fit }};">
```

---

### 2. Google Fonts選択機能を拡張

#### 問題
- フォント選択肢が5種類のみで少ない

#### 修正内容
**ファイル**: `sites/forms.py`

フォント選択肢を24種類に拡張：

```python
FONT_CHOICES = [
    # ゴシック系
    ('Noto Sans JP', 'Noto Sans JP（ゴシック）'),
    ('M PLUS 1p', 'M PLUS 1p（ゴシック）'),
    ('M PLUS Rounded 1c', 'M PLUS Rounded 1c（丸ゴシック）'),
    ('Kosugi Maru', 'Kosugi Maru（丸ゴシック）'),
    ('Zen Kaku Gothic New', 'Zen Kaku Gothic New（ゴシック）'),
    # 明朝系
    ('Noto Serif JP', 'Noto Serif JP（明朝）'),
    ('Sawarabi Mincho', 'Sawarabi Mincho（明朝）'),
    ('Zen Old Mincho', 'Zen Old Mincho（明朝）'),
    ('Shippori Mincho', 'Shippori Mincho（明朝）'),
    # デザイン系
    ('Zen Maru Gothic', 'Zen Maru Gothic（丸ゴシック）'),
    ('Kaisei Decol', 'Kaisei Decol（デコラティブ）'),
    ('Dela Gothic One', 'Dela Gothic One（太字）'),
    ('Reggae One', 'Reggae One（ポップ）'),
    ('RocknRoll One', 'RocknRoll One（ポップ）'),
    ('Yusei Magic', 'Yusei Magic（手書き風）'),
    ('Klee One', 'Klee One（手書き風）'),
    ('Hachi Maru Pop', 'Hachi Maru Pop（ポップ）'),
    # 英語フォント
    ('Roboto', 'Roboto（英語）'),
    ('Open Sans', 'Open Sans（英語）'),
    ('Lato', 'Lato（英語）'),
    ('Montserrat', 'Montserrat（英語）'),
    ('Poppins', 'Poppins（英語）'),
    ('Playfair Display', 'Playfair Display（英語セリフ）'),
]
```

**ファイル**: `templates/base.html`

Google Fontsの読み込みURLを拡張

---

### 3. プレビューの横幅を全画面に修正

#### 問題
- プレビューで各セクション（top以下）に無駄な余白がある

#### 修正内容
**ファイル**: `templates/sites/preview.html`

`max-w-4xl mx-auto`、`max-w-6xl mx-auto`、`max-w-7xl mx-auto` を削除し、`w-full px-4` に変更：

```html
<!-- 変更前 -->
<div class="max-w-4xl mx-auto px-4">

<!-- 変更後 -->
<div class="w-full px-4">
```

### マイグレーション
```bash
python manage.py makemigrations sites
python manage.py migrate
```

---

## 2025-12-26: 編集フォーム修正・プレビュー横幅調整

### 1. 編集フォームに画像設定フィールドを追加

#### 問題
- 画像サイズ調整機能がmodelsとformsに追加されたが、edit.htmlに反映されていなかった

#### 修正内容
**ファイル**: `templates/sites/edit.html`

各セクションに画像設定フィールドを追加：
- トップセクション: `hero_image_fit`, `hero_image_height`
- メインセクション: `image_fit`, `image_height`
- サブセクション: `image_fit`, `image_height`

```html
<!-- 画像設定 -->
<div class="divider my-6"></div>
<h3 class="text-sm font-semibold text-gray-700 mb-4">画像設定</h3>
<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
    <div class="form-group">
        <label class="form-label">画像表示モード</label>
        <select name="image_fit" class="form-select">
            <option value="cover">カバー（トリミング）</option>
            <option value="contain">全体表示</option>
            <option value="fill">引き伸ばし</option>
        </select>
    </div>
    <div class="form-group">
        <label class="form-label">画像高さ(px)</label>
        <input type="number" name="image_height" class="form-input">
    </div>
</div>
```

---

### 2. フォント選択を24種類に拡張（編集画面）

#### 問題
- forms.pyのFONT_CHOICESは24種類に拡張されたが、edit.htmlのselectタグはハードコードで3-5種類のみだった

#### 修正内容
**ファイル**: `templates/sites/edit.html`

全セクション（トップ/メイン/サブ/アクセス）のフォント選択を24種類に拡張：
- ゴシック系: Noto Sans JP, M PLUS 1p, M PLUS Rounded 1c, Kosugi Maru, Zen Kaku Gothic New
- 明朝系: Noto Serif JP, Sawarabi Mincho, Zen Old Mincho, Shippori Mincho
- デザイン系: Zen Maru Gothic, Kaisei Decol, Dela Gothic One, Reggae One, RocknRoll One, Yusei Magic, Klee One, Hachi Maru Pop
- 英語フォント: Roboto, Open Sans, Lato, Montserrat, Poppins, Playfair Display

`<optgroup>`タグでカテゴリ分けして表示

---

### 3. プレビューの横幅を調整

#### 問題
- メインセクションとアクセスセクションが全幅（w-full）になっており、コンテンツが広がりすぎていた

#### 修正内容
**ファイル**: `templates/sites/preview.html`

横幅を元に戻す：
```html
<!-- メインセクション -->
<!-- 変更前 -->
<div class="w-full px-4">

<!-- 変更後 -->
<div class="max-w-6xl mx-auto px-4">

<!-- アクセスセクション -->
<!-- 変更前 -->
<div class="w-full px-4">

<!-- 変更後 -->
<div class="max-w-4xl mx-auto px-4">
```

---

### 4. メインカルーセルのデフォルト高さを増加

#### 変更内容
**ファイル**: `templates/sites/edit.html`

メインセクションの画像高さのデフォルト値を400pxから500pxに変更
