from django.urls import path
from .views import *

urlpatterns = [
    path('', home_index, name='home.index.page'),
    path('contact-us', contact_page, name='contact.us.page'),
    # path('Partials/Site_Header_Partial', Site_Header_Partial, name='Site.Header.Partial'),
    # path('Partials/Site_Footer_Partial', Site_Footer_Partial, name='Site.Footer.Partial'),
]
