from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import re

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
        help_text="8~32文字の半角英数字と'_-'のみ許可",
    )
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if len(email) > 255:
            raise ValidationError('メールアドレスは255文字以下にしてください。')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if not re.match(r'^[a-zA-Z0-9_-]{8,32}$', password):
                raise ValidationError("パスワードは8~32文字の半角英数字と'_-のみ使用できます。")
        return password

    def clean_name(self):
        name = self.cleaned_data.get('first_name')
        if len(name) > 255:
            raise ValidationError("名前は255文字以内にしてください。")
        return name
