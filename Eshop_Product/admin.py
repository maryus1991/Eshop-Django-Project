from django.contrib import admin
from .models import Product, ProductCategory, ProductTag, ProductBrand, ProductVisit, ProductGallery
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    # readonly_fields = ['slug']
    prepopulated_fields = {
        'slug': ['name']
    }
    list_display = ['__str__', 'price', 'rating', 'is_active']
    list_filter = ['price', 'rating', 'is_active', 'id']
    list_editable = ['is_active', 'rating']


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductTag)
admin.site.register(ProductBrand)
admin.site.register(ProductVisit)
admin.site.register(ProductGallery)
