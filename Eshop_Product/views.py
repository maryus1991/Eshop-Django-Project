from django.shortcuts import redirect, reverse, render
from django.views.generic import ListView, DetailView, View
from django.db.models.aggregates import Count
from .models import Product, ProductCategory, ProductBrand


# from django.urls import reverse
# Create your views here.


class Product_List(ListView):
    template_name = 'Eshop_Product/Product_List.html'
    model = Product
    context_object_name = 'Products_List'
    paginate_by = 18

    def get_queryset(self):
        query = super().get_queryset()
        brand = self.kwargs.get('brand')
        category = self.kwargs.get('category')
        if brand is not None:
            query = Product.objects.filter(is_active=True, is_delete=False, brand__slug__iexact=brand).order_by('id').all()
        elif category is not None:
            query = Product.objects.filter(is_active=True, is_delete=False, category__slug__iexact=category,
                                   ).order_by('id').all()
        else:
            query = Product.objects.filter(is_active=True, is_delete=False).order_by('id').all()
        return query


class Product_Detail(DetailView):
    template_name = 'Eshop_Product/Product_Detail.html'
    model = Product
    context_object_name = 'Product_Detail'

    def get_context_data(self, **kwargs):
        con = super().get_context_data(**kwargs)
        request = self.request
        # con['is_favorite'] = True if int(self.object.id) == int(request.session['pid']) else False
        return con


class addProductToFavorite(View):
    def get(self, request, **kwargs):
        pid = request.GET['pid']
        request.session['pid'] = pid
        return redirect(reverse('product_detail_page', kwargs={'pk': pid}))


def Product_categories_partial(request):
    Product_Category = ProductCategory.objects.prefetch_related('children').filter(is_active=True, is_delete=False,
                                                                                   parent=None).all()
    Product_Brand = ProductBrand.objects.annotate(product_count=Count('product')).filter(is_active=True, is_deleted=False).all()
    # print(Product_Category)
    context = {
        'Product_Category': Product_Category,
        'Product_Brand': Product_Brand,
    }
    return render(request, 'Eshop_Product/Product_category_partial.html', context)
