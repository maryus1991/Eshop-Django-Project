from django.urls import path

from .views import *

urlpatterns = [
    path('add-Product-To-Order', addProductToOrder, name='add.Product.To.Order'),
    path('', user_basket, name='Orders.page'),
    path('remove', remove_item_content),
    path('Change-Count', ChangeOrderCount),
]
