from django.shortcuts import render
from .models import Product
from django.shortcuts import get_object_or_404
from django.db.models import Avg
# from django.urls import reverse
# Create your views here.


def Product_List(request):
    Product_list = Product.objects.filter(is_active=True).all().order_by('-rating')
    content = {
        'Products_List':Product_list,
    }
    return render(request, 'Eshop_Product/Product_List.html', content)


def Product_Details_By_ID(request, id):
    Product_Detail = get_object_or_404(Product, pk=id)
    return render(request, 'Eshop_Product/Product_Detail.html',
                  {'Product_Detail': Product_Detail})

def Product_Details_By_Slug(request, slug):
    Product_Detail = get_object_or_404(Product, slug=slug)
    return render(request, 'Eshop_Product/Product_Detail.html',
                  {'Product_Detail': Product_Detail})