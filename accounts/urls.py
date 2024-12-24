from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),              # ログイン画面
    path('admin/settings/', views.admin_settings, name='admin_settings'),  # 管理者設定画面
]
