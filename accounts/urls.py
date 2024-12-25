from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),              # ログイン画面
    path('admin/settings/', views.admin_settings, name='admin_settings'),  # 管理者設定画面
    path('account_list/', views.account_list, name='account_list'),
    path('account_delete/<int:user_id>/', views.account_delete, name='account_delete'),
    path('toggle_status/<int:user_id>/', views.toggle_status, name='toggle_status'),
    path('account_create/', views.account_create, name='account_create'),
]
