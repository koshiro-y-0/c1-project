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
