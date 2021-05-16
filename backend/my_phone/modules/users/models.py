from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """
    用户模型
    """
    phone = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    head_pic = models.ImageField(upload_to="head_pic", verbose_name="用户头像", blank=True, null=True)

    class Meta:
        db_table = "t_users"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
