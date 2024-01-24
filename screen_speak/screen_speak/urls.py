from django.contrib import admin  # Djangoの管理サイト機能をインポート
from django.urls import path, include  # URLパターン定義のための関数をインポート

urlpatterns = [
    path('admin/', admin.site.urls),  # Django管理サイトへのURLパターンを定義
    path('', include('flick_seeker.urls', namespace='flick_seeker')),  # 'flick_seeker'アプリケーションのURLパターンをプロジェクト全体のURL設定に含める
]
