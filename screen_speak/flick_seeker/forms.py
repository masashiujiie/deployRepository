from django import forms  # Djangoのフォーム機能をインポート
from django.contrib.auth.forms import UserCreationForm  # Djangoの標準ユーザー作成フォームをインポート
from django.contrib.auth import get_user_model  # 現在使用中のユーザーモデルを取得する関数をインポート
from django.core.exceptions import ValidationError  # フォームのバリデーションエラーを処理するための例外クラスをインポート
from django.utils.translation import gettext_lazy as _  # 国際化（多言語対応）のための翻訳機能をインポート

User = get_user_model()  # 現在アクティブなユーザーモデルを取得

class CustomUserCreationForm(UserCreationForm):
    # カスタムユーザー作成フォーム。UserCreationFormを拡張してカスタマイズ
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')  # メールアドレスフィールドを定義。ヘルプテキスト付き
    username = forms.CharField(max_length=150, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')  # ユーザー名フィールドを定義。ヘルプテキスト付き
    
    class Meta:
        model = User  # このフォームが使用するモデル
        fields = ('username','email')  # フォームで使用するフィールド
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # UserCreationFormのデフォルトのpasswordフィールドを削除
        if 'password1' in self.fields:
            del self.fields['password1']
        if 'password2' in self.fields:
            del self.fields['password2']
        
class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
