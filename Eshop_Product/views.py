from django.db.models import Q
from django.db.models.aggregates import Count
from django.shortcuts import redirect, reverse, render
from django.views.generic import ListView, DetailView, View

from utils.get_ip import get_client_ip
from utils.list_slicer import list_slicer
from .models import Product, ProductCategory, ProductBrand, ProductVisit


# from django.urls import reverse
# Create your views here.


class Product_List(ListView):
    template_name = 'Eshop_Product/Product_List.html'
    model = Product
    context_object_name = 'Products_List'
    paginate_by = 18

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['S_Price'] = self.request.GET.get('S_Price') or 0
        context['E_Price'] = self.request.GET.get('E_Price') or 10000000000
        return context

    def get_queryset(self):
        query = super().get_queryset()
        brand = self.kwargs.get('brand')
        category = self.kwargs.get('category')

        if self.request.GET.get('price'):
            price: str = str(self.request.GET.get('price'))
        else:
            price: str = '0,100000000'
        S_Price = price.split(',')[0]
        product = Product.objects.filter(is_delete=False, is_active=True).order_by('-price').first()
        E_Price = price.split(',')[1]

        if brand is not None:
            query = Product.objects.filter(is_active=True, is_delete=False, brand__slug__iexact=brand).order_by(
                'id').all()
        elif category is not None:
            query = Product.objects.filter(is_active=True, is_delete=False, category__slug__iexact=category, ).order_by(
                'id').all()
        elif S_Price is not None:
            query = Product.objects.filter(is_active=True, is_delete=False, price__gte=S_Price)
        elif E_Price is not None:
            query = Product.objects.filter(is_active=True, is_delete=False, price__lte=E_Price)
        else:
            query = Product.objects.filter(is_active=True, is_delete=False).order_by('id').all()
        return query


class Product_Detail(DetailView):
    template_name = 'Eshop_Product/Product_Detail.html'
    model = Product
    context_object_name = 'Product_Detail'

    def get_context_data(self, **kwargs):
        user_ip = get_client_ip(self.request)
        con = super().get_context_data(**kwargs)
        product = self.get_object()
        request = self.request
        user_id = None
        if request.user.is_authenticated:
            user_id = self.request.user.id
        if not ProductVisit.objects.filter(ipaddress=user_ip, product=product).exists():
            ProductVisit.objects.create(ipaddress=user_ip, product=product, user_id=user_id).save()
        # con['is_favorite'] = True if int(self.object.id) == int(request.session['pid']) else False
        con['tags'] = self.object.product_tags.filter(is_delete=False, is_active=True).all()
        galleries = list(self.object.galleries.filter(is_delete=False, is_active=True).all())
        galleries.insert(0, self.object)
        con['galleries'] = list_slicer(galleries, 3)
        con['releted_product'] = list_slicer(list(Product.objects.filter(Q(is_delete=False, is_active=True),
                                                                         Q(brand_id=self.object.brand_id),

                                                                         ).exclude(pk=self.object.id
                                                                                   ).all()), 3)
        return con


class addProductToFavorite(View):
    def get(self, request, **kwargs):
        pid = request.GET['pid']
        request.session['pid'] = pid
        return redirect(reverse('product_detail_page', kwargs={'pk': pid}))


def Product_categories_partial(request, E_Price=100000000, S_Price=0):
    Product_Category = ProductCategory.objects.prefetch_related('children').filter(is_active=True, is_delete=False,
                                                                                   parent=None).all()
    Product_Brand = ProductBrand.objects.annotate(
        product_count=Count('product', filter=Q(product__is_active=True, product__is_delete=False))).filter(
        is_active=True,
        is_deleted=False).all()

    context = {'Product_Category': Product_Category, 'Product_Brand': Product_Brand, 'S_Price': S_Price,
               'E_Price': E_Price}
    return render(request, 'Eshop_Product/Product_category_partial.html', context)
