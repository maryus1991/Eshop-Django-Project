from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from Eshop_Product.models import Product
from .models import Order, OrderDetail


def addProductToOrder(request):
    try:
        if request.user.is_authenticated:
            pid = request.GET.get('pid')
            count = int(request.GET.get('count'))
            if count > 0:
                product = Product.objects.filter(pk=pid, is_active=True, is_delete=False).first()
                if product is not None:
                    user_order = Order.objects.get_or_create(user_id=request.user.id, is_active=True, is_paid=False)
                    user_order_detail = user_order[0].details.filter(product_id=product.id, is_active=True).first()
                    if user_order_detail is not None:
                        user_order_detail.count += count
                        user_order_detail.save()
                        return JsonResponse({'status': 200})
                    else:
                        order_detail = OrderDetail.objects.create(count=count, product_id=product.id,
                                                                  order_id=user_order[0].id)
                        order_detail.save()
                        return JsonResponse({'status': 200})
                else:
                    return JsonResponse({'status': 'محصول مورد نظر پیدا نشده است '})
            else:
                return JsonResponse({'status': 'مقدار باید بیشتر از صفر باشد'})
        else:
            return JsonResponse({'status': 'کاربر ثبت نام نکرده است '})
    except:
        raise Http404()


def user_basket(request):
    user_order, created = Order.objects.prefetch_related('details').get_or_create(user_id=request.user.id,
                                                                                  is_active=True, is_paid=False)
    total = 0

    for order_detail in user_order.details.exclude(is_active=False).all():
        total += float(order_detail.count) * order_detail.product.price
        order_detail.final_price = float(order_detail.count) * order_detail.product.price
        order_detail.save()
    context = {
        'user_order': user_order.details.exclude(is_active=False).all(),
        'total': total,
    }
    return render(request, 'Eshop_Order/user_bascket.html', context)


def remove_item_content(request):
    user_order, created = Order.objects.prefetch_related('details').get_or_create(user_id=request.user.id,
                                                                                  is_active=True, is_paid=False)
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({'status': 'سبد پیدا نشد'})
    else:
        detail = user_order.details.filter(id=detail_id, is_active=True).first()
        if detail is None:
            return JsonResponse({'status': 'سبد پیدا نشد '})
        else:
            detail.is_active = False
            detail.save()

    total = 0
    for order_detail in user_order.details.exclude(is_active=False).all():
        total += float(order_detail.count) * order_detail.product.price
        order_detail.final_price = float(order_detail.count) * order_detail.product.price
        order_detail.save()
    context = {
        'user_order': user_order.details.exclude(is_active=False).all(),
        'total': total,
    }
    print('wwwwwwwwww')
    data = render_to_string('Eshop_Order/user_backet_for_ajax.html', context)
    return JsonResponse({'status': 200, 'data': data})