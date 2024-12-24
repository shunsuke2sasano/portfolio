from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import AdminSettingsForm

# 管理者専用アクセスのチェック
def admin_check(user):
    return user.is_staff or user.is_superuser

def login_view(request):
    """
    管理者と一般ユーザー共通のログインビュー
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # フォームが有効な場合、ユーザーを認証
            user = form.get_user()
            login(request, user)
            # ログイン後のリダイレクト先をユーザーのタイプで変更
            if user.is_staff or user.is_superuser:
                return redirect('dashboard:admin_dashboard')
            else:
                return redirect('dashboard:user_dashboard')
        else:
            # 認証失敗時にエラーメッセージを表示
            messages.error(request, "ログインに失敗しました。ユーザー名またはパスワードが正しくありません。")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

@login_required
@user_passes_test(admin_check)  # 管理者のみアクセス許可
def admin_settings(request):
    """
    管理者設定画面
    """
    if request.method == 'POST':
        form = AdminSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data.get('password'):
                user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request, "設定が更新されました。")
        else:
            messages.error(request, "入力にエラーがあります。")
    else:
        form = AdminSettingsForm(instance=request.user)

    return render(request, 'accounts/admin_settings.html', {'form': form})
