from django.urls import path
from .views import *

urlpatterns = [
    path('', home_index, name='home.index.page'),
    path('contact-us', contact_page_views.as_view(), name='contact.us.page'),
    path('About_page', About_page, name='About.us.page'),
]
