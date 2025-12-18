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
]
