from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

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
            if user.is_admin:
                return redirect('dashboard:admin_dashboard')
            else:
                return redirect('dashboard:user_dashboard')
        else:
            # 認証失敗時にエラーメッセージを表示
            messages.error(request, "ログインに失敗しました。ユーザー名またはパスワードが正しくありません。")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})
