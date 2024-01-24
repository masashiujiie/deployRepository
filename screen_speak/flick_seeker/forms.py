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
    # パスワードフィールド1。カスタムヘルプテキスト付き
    password1 = forms.CharField( 
        label=_("Password"),
        widget=forms.PasswordInput,  # パスワード入力のためのウィジェットを使用
        help_text=_("Your password must be at least 8 characters long, and contain at least one uppercase letter, one lowercase letter, one digit, and one special character."),
    )
    
    # パスワードフィールド2（確認用）。カスタムヘルプテキスト付き
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,  # パスワード入力のためのウィジェットを使用
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User  # このフォームが使用するモデル
        fields = ('username','email', 'password1', 'password2')  # フォームで使用するフィールド

    def clean_password1(self):
        # パスワード1の検証メソッド
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            # パスワードが8文字未満の場合はエラーを発生させる
            raise ValidationError("Password must be at least 8 characters long and meet the specified criteria.")
        return password1

    def clean_password2(self):
        # パスワード2の検証メソッド
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            # パスワード1とパスワード2が一致しない場合はエラーを発生させる
            raise forms.ValidationError("パスワードが一致しません")  # パスワードが一致しない場合にエラーを発生
        return password2
