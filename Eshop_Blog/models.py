from django.db import models
from jalali_date import date2jalali

from Eshop_Account.models import User


# Create your models here.
class Blog_Category(models.Model):
    parent = models.ForeignKey('Blog_Category', on_delete=models.CASCADE, verbose_name='دسته بندی', null=True,
                               blank=True, related_name='children')
    title = models.CharField(max_length=100, verbose_name='عنوان')
    url_title = models.CharField(max_length=100, verbose_name='عنوان لینک', unique=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_delete = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, allow_unicode=True,
                            verbose_name='عنوان در لینک')
    description = models.TextField(verbose_name='توضیحات')
    img = models.ImageField(upload_to='images/blog/', verbose_name='عکس مقاله')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_delete = models.BooleanField(default=False, verbose_name='حذف')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    select_categories = models.ManyToManyField(Blog_Category, verbose_name='دسته بندی')
    publish_date = models.DateTimeField(auto_now_add=True, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده', editable=False)

    def __str__(self):
        return self.title

    def get_jalali_create_date(self):
        return date2jalali(self.publish_date).strftime('%Y/%m/%d')

    def get_jalali_create_time(self):
        return self.publish_date.strftime('%H:%M')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'


class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='مقاله')
    parent = models.ForeignKey('BlogComment', on_delete=models.CASCADE,
                               verbose_name='زیر کامنت', null=True,
                               blank=True, related_name='children')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    create_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='تاریخ ثبت')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    text = models.TextField(verbose_name='متن')
    is_delete = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'کامنت '
        verbose_name_plural = 'کامنت ها'

    def get_jalali_create_date(self):
        return date2jalali(self.create_date).strftime('%Y/%m/%d')

    def get_jalali_create_time(self):
        return self.create_date.strftime('%H:%M')
