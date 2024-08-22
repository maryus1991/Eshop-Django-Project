from django.db import models

from Eshop_Account.models import User
from Eshop_Product.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(default=False, verbose_name='وضعیت پرداخت')
    payment_date = models.DateTimeField(blank=True, null=True, verbose_name='تاریخ پرداخت')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    def get_final_price(self):
        total_price = 0
        if self.is_paid:
            for order_detail in self.details.filter(is_active=True).all():
                total_price += float(order_detail.final_price) * float(order_detail.count)
        else:
            for order_detail in self.details.filter(is_active=True).all():
                total_price += float(order_detail.product.price) * float(order_detail.count)
        return total_price

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید کاربران'

    def __str__(self):
        return str(self.user)


class OrderDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید', related_name='details')
    final_price = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True,
                                      verbose_name='قیمت نهایی تکی محصول')
    count = models.DecimalField(max_digits=100, decimal_places=2, verbose_name='تعداد')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = 'جزییات سبد خرید'
        verbose_name_plural = 'جزییات سبد های خرید'
