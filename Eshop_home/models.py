from django.db import models


class Eshop_Contact_Us(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    title = models.CharField(max_length=100, verbose_name='موضوع')
    message = models.TextField()
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_deleted = models.BooleanField(default=False, verbose_name='حذف بشود ؟')
    is_read_by_admin = models.BooleanField(default=False, verbose_name='خوانده شده توسط ادمین')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساختن')
    response = models.TextField(null=True, blank=True, verbose_name='پاسخ')

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'لیست تماس با ما'

    def __str__(self):
        return self.title
