from django.utils.text import slugify
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class ProductCategory(models.Model):
    title = models.CharField(db_index=True,max_length=100, verbose_name='عنوان')
    slug = models.SlugField(db_index=True, unique=True, blank=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_delete = models.BooleanField(default=False, verbose_name="حذف کردن")

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        unique_together = (('slug', 'id', 'is_active', 'is_delete'),)


class ProductTag(models.Model):
    title = models.CharField(db_index=True, max_length=100, verbose_name='عنوان')
    slug = models.CharField(max_length=100,db_index=True, unique=True,verbose_name='عنوان در url')
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_delete = models.BooleanField(default=False, verbose_name="حذف کردن")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ ها'
        unique_together = (('slug', 'id', 'is_active', 'is_delete'),)


class Product(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='نام')
    price = models.FloatField(verbose_name='قیمت')
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name='ریت ها')
    description = models.TextField(db_index=True, verbose_name='توضیحات اصلی')
    short_description = models.TextField(db_index=True, verbose_name='توضیحات کوتاه')
    slug = models.SlugField(db_index=True, unique=True, blank=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    category = models.ManyToManyField(ProductCategory, db_index=True,  null=True, blank=True,
                                      related_name='Products', verbose_name='کتگوری ها')
    product_tags = models.ManyToManyField(ProductTag, blank=True, related_name='Tags', null=True
                                          , verbose_name='تگ های محصول')
    is_delete = models.BooleanField(default=False, verbose_name="حذف کردن")

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        unique_together = (('slug', 'id', 'is_active', 'is_delete'),)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.id})({self.price})'
