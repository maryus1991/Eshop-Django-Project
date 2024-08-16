from django.shortcuts import redirect, reverse
from django.views.generic import ListView, DetailView, View

from .models import Product


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

    def get_context_data(self, **kwargs):
        con = super().get_context_data(**kwargs)
        request = self.request
        con['is_favorite'] =  str(self.object.id) in str(request.session['pid'])
        return con



class addProductToFavorite(View):
    def get(self, request, **kwargs):
        pid = request.GET['pid']
        request.session['pid'] = pid
        return redirect(reverse('product_detail_page', kwargs={'pk': pid}))
