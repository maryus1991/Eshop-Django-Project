from django.urls import path
from .views import Product_List, Product_Details_By_ID, Product_Details_By_Slug


urlpatterns = [
    path('', Product_List, name='product_list_page'),
    path("<int:id>", Product_Details_By_ID, name='product_detail_page'),
    path("<str:slug>", Product_Details_By_Slug, name='product_detail_page_slug'),
]