from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify

from Eshop_Account.models import User


class ProductBrand(models.Model):
    title = models.CharField(max_length=100, verbose_name="نام برند", db_index=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='نام در url')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_deleted = models.BooleanField(default=False, verbose_name="حذف کردن")
    description = models.TextField(verbose_name="توضیحات برند")

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برندها'

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    title = models.CharField(db_index=True, max_length=100, verbose_name='عنوان')
    slug = models.SlugField(db_index=True, unique=True, blank=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_delete = models.BooleanField(default=False, verbose_name="حذف کردن")
    parent = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, related_name='children', null=True,
                               blank=True)

    def __str__(self):
        return self.slug

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class ProductTag(models.Model):
    title = models.CharField(db_index=True, max_length=100, verbose_name='عنوان')
    slug = models.CharField(max_length=100, db_index=True, unique=True, verbose_name='عنوان در url')
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
    category = models.ManyToManyField(ProductCategory, db_index=True, related_name='Products', verbose_name='کتگوری ها',
                                      blank=True, null=True)
    product_tags = models.ManyToManyField(ProductTag, related_name='Tags', verbose_name='تگ های محصول', blank=True,
                                          null=True)
    is_delete = models.BooleanField(default=False, verbose_name="حذف کردن")
    brand = models.ForeignKey(ProductBrand, null=True, blank=True, verbose_name='برند', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image/product/', null=True, blank=True, verbose_name='تصویر محصول')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        unique_together = (('slug', 'id', 'is_active', 'is_delete'),)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.id})({self.price})'


class ProductVisit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول', related_name='visits')
    ipaddress = models.GenericIPAddressField(verbose_name='ای پی کاربر')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='کاربر')

    def __str__(self):
        return f'{self.product.id} => ({self.ipaddress})'

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدید محصولات'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='گالری تصاویر',
                                related_name='galleries')
    image = models.ImageField(upload_to='images/galleries', verbose_name='عکس')
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_delete = models.BooleanField(default=False, verbose_name="حذف کردن")

    def __str__(self):
        return f'{self.product.name}/({self.id})'

    class Meta:
        verbose_name = 'گالری'
        verbose_name_plural = 'گالریها'
