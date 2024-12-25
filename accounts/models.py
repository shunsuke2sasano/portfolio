from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)  # 管理者フラグ
    name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(max_length=1500, blank=True, null=True)  
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)