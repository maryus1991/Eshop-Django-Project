from django.urls import path

from .views import BlogListView, BlogDetailView, BlogListView_by_category

urlpatterns = [
    path('', BlogListView.as_view(), name='blog.list'),
    path('<slug:slug>', BlogDetailView.as_view(), name='detail.blog.list'),
    path('category/<slug:slug>', BlogListView_by_category.as_view(), name='category.blog.list'),
]
