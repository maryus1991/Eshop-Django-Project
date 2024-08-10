from django.urls import path
from .views import *

urlpatterns = [
    path('', home_index, name='home.index.page'),
    path('contact-us', contact_page, name='contact.us.page'),
    path('contact-us/add', add_Eshop_Contact_Us, name='add.Eshop.Contact.Us'),
]
