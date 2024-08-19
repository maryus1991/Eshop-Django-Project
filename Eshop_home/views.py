from django.db.models import Q
from django.db.models.aggregates import Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from Eshop_Product.models import Product, ProductCategory
from Eshop_Setting.models import SiteSettings
from utils.list_slicer import list_slicer
from .forms import ContactUsForm
from .models import Eshop_Slider


def home_index(request):
    # print(list_slicer(Product.objects.filter(is_active=True, is_delete=False).all()[:8]))
    latest_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:8]
    most_popular_products = Product.objects.filter(is_active=True, is_delete=False).order_by('rating')[:8]
    most_visited_products = Product.objects.filter(is_active=True, is_delete=False).annotate(
        visit_count=Count('visits')).order_by('-visit_count')[:8]
    Product_Category = list(
        ProductCategory.objects.annotate(count_product=Count('Products', filter=Q(Products__is_active=True, Products__is_delete=False))).filter(is_active=True,
                                                                                 is_delete=False)[:10])
    categories_product = []
    for category in Product_Category:
        print(category.count_product)
        if category.count_product > 0:
            item = {
                'id': category.id,
                'title': category.title,
                'products': list(
                    category.Products.filter(is_active=True, is_delete=False).order_by('-id').all()[:4])
            }
            categories_product.append(item)
        else:
            pass

    context = {
        'slider': Eshop_Slider.objects.filter(is_active=True, is_delete=False).all()[:2],
        'SiteSettings': SiteSettings.objects.filter(is_main_setting=True, is_active=True).first(),
        'latest_products': list_slicer(latest_products),
        'most_popular_products': list_slicer(most_popular_products),
        'most_visited_products': list_slicer(most_visited_products),
        'categories_product': categories_product,
    }

    return render(request, 'Eshop_home/Eshop_home_index.html', context)


def About_page(request):
    # site_settings =
    context = {
        'SiteSettings': SiteSettings.objects.filter(is_main_setting=True, is_active=True).first()
    }
    return render(request, 'Eshop_home/About.html', context)


class contact_page_views(CreateView):
    form_class = ContactUsForm
    template_name = 'Eshop_home/Eshop_home_Contact-Us.html'
    success_url = reverse_lazy('contact.us.page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['SiteSettings'] = SiteSettings.objects.filter(is_main_setting=True, is_active=True).first()
        return context


def Site_Header_Partial(request):
    context = {'SiteSettings': SiteSettings.objects.filter(is_main_setting=True, is_active=True).first()}
    return render(request, 'Base/HeaderBase.html', context)


def Site_Footer_Partial(request):
    context = {'SiteSettings': SiteSettings.objects.filter(is_main_setting=True, is_active=True).first()}
    return render(request, 'Base/FooterBase.html', context)
