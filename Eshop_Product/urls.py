from django.urls import path

from .views import Product_List, Product_Detail, addProductToFavorite

urlpatterns = [
    path('', Product_List.as_view(), name='product_list_page'),
    path("addtofavrite", addProductToFavorite.as_view(), name='product_detail_page_Fp'),
    path("<int:pk>", Product_Detail.as_view(), name='product_detail_page'),
    path("<slug:slug>", Product_Detail.as_view(), name='product_detail_page_slug'),
    path("brand/<slug:brand>", Product_List.as_view(), name='brand_list_page_slug'),
    path("category/<slug:category>", Product_List.as_view(), name='category_list_page_slug'),
]
