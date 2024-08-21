from django.urls import path
from .views import UserDashBord_editUser_Profile_page, UserDashBord_Change_pass, user_shopping_history, order_detail

urlpatterns = [
    path('', UserDashBord_editUser_Profile_page.as_view(), name='dashboard.user'),
    path('edit/', UserDashBord_editUser_Profile_page.as_view(), name='UserDashBord_editUser_Profile_page'),
    path('changePass/', UserDashBord_Change_pass.as_view(), name='UserDashBord.Change.pass'),
    path('my-shopping/', user_shopping_history.as_view(), name='user.shopping.page'),
    path('my-shopping-history/<int:oid>', order_detail, name='order.detail.shopping.page'),
]