"""
URL configuration for Eshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import settings

urlpatterns = [path('admin/', admin.site.urls),
               path('product/', include('Eshop_Product.urls')),
               path('', include('Eshop_home.urls')),
               path('auth/', include('Eshop_Account.urls')),
               path('blog/', include('Eshop_Blog.urls')),
               path('user/', include('Eshop_User_Profile.urls')),
               path('order/', include('Eshop_Order.urls')),
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
