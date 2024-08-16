from django.db import models


# Create your models here.
class SiteSettings(models.Model):
    site_name = models.CharField(max_length=50, verbose_name='نام سایت')
    site_url = models.CharField(max_length=50, verbose_name='ادرس سایت')
    addr = models.CharField(max_length=50, verbose_name='ادرس')
    phone = models.CharField(max_length=50, verbose_name='شماره تلفن')
    phone_s = models.CharField(max_length=50, verbose_name='شماره تلفن ثابت')
    email = models.CharField(max_length=50, verbose_name='ایمیل سایت ')
    copyright = models.TextField(verbose_name='متن کپی رایت')
    site_logo = models.ImageField(upload_to='images/site_setting_logo/', verbose_name='لوگو')
    about_us = models.TextField(verbose_name='درباره ما')
    is_active = models.BooleanField(default=True, verbose_name='فعال بودن')
    is_deleted = models.BooleanField(default=False, verbose_name='حدف کردن')
    is_main_setting = models.BooleanField(default=False, verbose_name='تنظیمات اصلی بودن')

    class Meta:
        verbose_name = 'تنظمات سایت'
        verbose_name_plural = 'تنظمات سایت'

    def __str__(self):
        return self.site_name