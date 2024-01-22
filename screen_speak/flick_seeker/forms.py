from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    # カスタムユーザー作成フォーム

    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        help_text=_("Your password must be at least 8 characters long, and contain at least one uppercase letter, one lowercase letter, one digit, and one special character."),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password1(self):
        # パスワード1の検証
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long and meet the specified criteria.")
        return password1

    def clean_password2(self):
        # パスワード2の検証
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("パスワードが一致しません")  # パスワードが一致しない場合にエラーを発生
        return password2
