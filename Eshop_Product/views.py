from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product
from django.shortcuts import get_object_or_404
from django.db.models import Avg


# from django.urls import reverse
# Create your views here.


class Product_List(ListView):
    template_name = 'Eshop_Product/Product_List.html'
    model = Product
    context_object_name = 'Products_List'
    paginate_by = 18

    def get_queryset(self):
        return Product.objects.filter(is_active=True, is_delete=False).order_by('id').all()


class Product_Detail(DetailView):
    template_name = 'Eshop_Product/Product_Detail.html'
    model = Product
    context_object_name = 'Product_Detail'

#
# def Product_Details_By_ID(request, id):
#     Product_Detail = get_object_or_404(Product, pk=id)
#     return render(request, 'Eshop_Product/Product_Detail.html',
#                   {'Product_Detail': Product_Detail})
#
#
# def Product_Details_By_Slug(request, slug):
#     Product_Detail = get_object_or_404(Product, slug=slug)
#     return render(request, 'Eshop_Product/Product_Detail.html',
#                   {'Product_Detail': Product_Detail})
