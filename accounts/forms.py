from django import forms
from django.core.exceptions import ValidationError
import re
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminSettingsForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={'invalid': '有効なメールアドレスを入力してください。'}
    )
    password = forms.CharField(
        max_length=32,
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="8~32文字の半角英数字と'_'、'-'のみ使用可能"
    )
    account_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'account_name']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and not re.match(r'^[a-zA-Z0-9_-]{8,32}$', password):
            raise ValidationError("パスワードは8~32文字の半角英数字と'_'、'-'のみ使用可能です。")
        return password
