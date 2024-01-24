from django.contrib import admin  # Djangoの管理サイト機能をインポート
from .models import User  # 同じアプリケーション内のUserモデルをインポート
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin  # DjangoのデフォルトUserAdminをインポート

class UserAdmin(DefaultUserAdmin):
    # デフォルトのUserAdmin設定をカスタマイズするクラス
    model = User  # このUserAdminが扱うモデルを指定
    list_display = ['email', 'is_staff', 'is_active']  # 管理画面のリスト表示に使用するフィールド
    list_filter = ['email', 'is_staff', 'is_active']  # リスト画面でフィルター可能なフィールド
    search_fields = ['email']  # リスト画面で検索可能なフィールド
    ordering = ['email']  # リスト画面でのデフォルトの並び順
    
admin.site.register(User, UserAdmin)  # Djangoの管理サイトにUserモデルとUserAdminを登録

