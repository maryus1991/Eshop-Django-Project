from django.urls import path
from .views import UserDashBord, UserDashBord_editUser_Profile_page, UserDashBord_Change_pass

urlpatterns = [
    path('', UserDashBord_editUser_Profile_page.as_view(), name='dashboard.user'),
    path('edit/', UserDashBord_editUser_Profile_page.as_view(), name='UserDashBord_editUser_Profile_page'),
    path('changePass/', UserDashBord_Change_pass.as_view(), name='UserDashBord.Change.pass'),
]