from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)  # 管理者フラグ
    account_name = models.CharField(max_length=255, blank=True, null=True)