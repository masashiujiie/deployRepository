from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

class UserAdmin(DefaultUserAdmin):
    # デフォルトのUserAdmin設定をオーバーライド
    model = User
    list_display = ['email', 'is_staff', 'is_active']
    list_filter = ['email', 'is_staff', 'is_active']
    search_fields = ['email']
    ordering = ['email']
    
admin.site.register(User, UserAdmin)
