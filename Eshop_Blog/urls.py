from django.urls import path

from .views import BlogListView, BlogDetailView, BlogListView_by_category, add_blog_comments

urlpatterns = [
    path('', BlogListView.as_view(), name='blog.list'),
    path('add-blog-comments', add_blog_comments, name='add.blog.comments.js'),
    path('<slug:slug>', BlogDetailView.as_view(), name='detail.blog.list'),
    path('category/<slug:slug>', BlogListView_by_category.as_view(), name='category.blog.list'),
]
