from django.contrib import admin

from .models import Blog_Category, Blog, BlogComment


# Register your models here.
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['parent', 'title', 'url_title', 'is_active']
    list_editable = ['title', 'url_title', 'is_active']


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active', 'author']

    def save_model(self, request, obj, form, change):
        if not obj:
            obj.author = request.user
            obj.save()
        return super().save_model(request, obj, form, change)


admin.site.register(Blog_Category, BlogCategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogComment)
