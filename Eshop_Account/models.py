from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name='تلفن همراه')
    is_verified = models.BooleanField(default=False, verbose_name='تایید شده')
    is_deleted = models.BooleanField(default=False, verbose_name='حذف کردن')
    email_verified = models.BooleanField(default=False, verbose_name='تایید ایمیل')
    mobile_verified = models.BooleanField(default=False, verbose_name='تایید شماره')
    email_active_code = models.CharField(max_length=100, blank=True, null=True, verbose_name='کد تایید ایمیل')
    mobile_active_code = models.CharField(max_length=100, blank=True, null=True, verbose_name='کد تایید شماره همراه')
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    about_user = models.TextField(verbose_name='درباره کاربر', blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
