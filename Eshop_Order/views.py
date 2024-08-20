from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.template.loader import render_to_string

from Eshop_Product.models import Product
from .models import Order, OrderDetail


@login_required
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


@login_required
def user_basket(request):
    user_order, created = Order.objects.prefetch_related('details').get_or_create(user_id=request.user.id,
                                                                                  is_active=True, is_paid=False)
    context = {
        'user_order': user_order.details.exclude(is_active=False).all(),
        'total': user_order.get_final_price(),
    }
    return render(request, 'Eshop_Order/user_bascket.html', context)


@login_required
def remove_item_content(request):
    user_order, created = Order.objects.prefetch_related('details').get_or_create(user_id=request.user.id,
                                                                                  is_active=True, is_paid=False)
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({'status': 'سبد پیدا نشد'})
    else:
        detail = user_order.details.filter(id=detail_id, is_active=True, order__is_active=True,
                                           order__is_paid=False, order__user_id=request.user.id
                                           ).first()
        if detail is None:
            return JsonResponse({'status': 'سبد پیدا نشد '})
        else:
            detail.is_active = False
            detail.save()
    context = {
        'user_order': user_order.details.exclude(is_active=False).all(),
        'total': user_order.get_final_price(),
    }

    data = render_to_string('Eshop_Order/user_backet_for_ajax.html', context)
    return JsonResponse({'status': 200, 'data': data})


@login_required
def ChangeOrderCount(request):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({'status': 'محصول پیدا نشد'})

    detail = OrderDetail.objects.filter(id=detail_id, is_active=True, order__is_active=True, order__is_paid=False
                                        , order__user_id=request.user.id).first()

    if detail is None:
        return JsonResponse({'status': 'سبد پیدا نشد'})

    if state == 'i':
        detail.count += 1
        detail.save()
    elif state == 'd':
        if detail.count <= 1:
            detail.is_active = False
            detail.save()
        elif detail.count > 1:
            detail.count -= 1
            detail.save()
        else:
            return JsonResponse({'status': 'مشکلی پیش اومد'})
    else:
        return JsonResponse({'status': 'یافت نشد'})

    user_order, created = Order.objects.prefetch_related('details').get_or_create(user_id=request.user.id,
                                                                                  is_active=True, is_paid=False)

    context = {
        'user_order': user_order.details.exclude(is_active=False).all(),
        'total': user_order.get_final_price(),
    }
    data = render_to_string('Eshop_Order/user_backet_for_ajax.html', context)
    return JsonResponse({'status': 200, 'data': data})
