from django import forms
from django.core.exceptions import ValidationError
import re
from django.contrib.auth import get_user_model

User = get_user_model()

def validate_hiragana(value):
    if not re.fullmatch(r'^[\u3040-\u309Fー]+$', value):
        raise ValidationError('ふりがなはひらがなのみで入力してください。')

class AdminSettingsForm(forms.ModelForm):
    account_type = forms.ChoiceField(
        choices=[('general', '一般'), ('admin', '管理者')],
        widget=forms.RadioSelect,
        required=True,
    )
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
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    furigana = forms.CharField(
        max_length=255,
        required=False,
        validators=[validate_hiragana],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    gender = forms.ChoiceField(
        choices=[('male', '男性'), ('female', '女性')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )
    age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        max_value=999,
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'furigana', 'gender', 'age', 'bio', 'profile_image']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and not re.match(r'^[a-zA-Z0-9_-]{8,32}$', password):
            raise ValidationError("パスワードは8~32文字の半角英数字と'_'、'-'のみ使用可能です。")
        return password

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if image and image.size > 2 * 1024 * 1024:  # 2MB
            raise ValidationError("画像サイズは2MB以内にしてください。")
        return image