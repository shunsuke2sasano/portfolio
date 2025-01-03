from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import AdminSettingsForm, AccountForm

User = get_user_model()

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

@login_required
@user_passes_test(admin_check)
def account_list(request):
    accounts = User.objects.all()
    paginator = Paginator(accounts, 5)  # 1ページあたり5件
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/account_list.html', {'page_obj': page_obj})

@login_required
@user_passes_test(admin_check)
def account_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "アカウントを削除しました。")
        return redirect('accounts:account_list')

@login_required
@user_passes_test(admin_check)
def toggle_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f"アカウントのステータスを{'有効化' if user.is_active else '無効化'}しました。")
    return redirect('accounts:account_list')

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def account_create(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES)
        if form.is_valid():
            account_type = form.cleaned_data.get('account_type')
            user = form.save(commit=False)
            if account_type == 'admin':
                user.is_staff = True
                user.is_superuser = True
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request, "アカウントが作成されました。")
            return redirect('accounts:account_list')
        else:
            messages.error(request, "入力にエラーがあります。")
    else:
        form = AccountForm()

    return render(request, 'accounts/account_create.html', {'form': form})

@login_required
@user_passes_test(admin_check)
def account_delete_list(request):
    # ステータスが無効（削除された状態）のアカウントを取得
    deleted_accounts = User.objects.filter(is_active=False)
    return render(request, 'accounts/account_delete_list.html', {'accounts': deleted_accounts})

@login_required
@user_passes_test(admin_check)
def account_delete_permanently(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()  # 完全削除
        messages.success(request, "アカウントを完全に削除しました。")
        return redirect('accounts:account_delete_list')

@login_required
@user_passes_test(admin_check)
def account_restore(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.is_active = True  # アクティブ化
        user.save()
        messages.success(request, "アカウントを復元しました。")
        return redirect('accounts:account_delete_list')