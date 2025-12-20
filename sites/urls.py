from django.urls import path
from . import views

app_name = 'sites'

urlpatterns = [
    # サイト一覧
    path('<int:user_id>/', views.site_list, name='site_list'),

    # サイト新規作成
    path('<int:user_id>/create/', views.site_create, name='site_create'),

    # サイト編集
    path('<int:user_id>/<int:site_id>/', views.site_edit, name='site_edit'),

    # プレビュー
    path('preview/<int:site_id>/', views.site_preview, name='site_preview'),

    # セクション保存エンドポイント
    path('<int:user_id>/<int:site_id>/save/basic/', views.save_basic, name='save_basic'),
    path('<int:user_id>/<int:site_id>/save/top/', views.save_top, name='save_top'),
    path('<int:user_id>/<int:site_id>/save/main/', views.save_main, name='save_main'),
    path('<int:user_id>/<int:site_id>/save/sub/', views.save_sub, name='save_sub'),
    path('<int:user_id>/<int:site_id>/save/access/', views.save_access, name='save_access'),
    path('<int:user_id>/<int:site_id>/save/sns/', views.save_sns, name='save_sns'),

    # HTMXプレビュー更新エンドポイント
    path('preview/<int:site_id>/header/', views.preview_header, name='preview_header'),
    path('preview/<int:site_id>/top/', views.preview_top, name='preview_top'),
    path('preview/<int:site_id>/main/', views.preview_main, name='preview_main'),
    path('preview/<int:site_id>/sub/', views.preview_sub, name='preview_sub'),
    path('preview/<int:site_id>/access/', views.preview_access, name='preview_access'),
]
