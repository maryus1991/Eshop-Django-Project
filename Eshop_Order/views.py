import datetime
from django.shortcuts import render, reverse, redirect
from django.conf import settings
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
                        user_order_detail.final_price = float(user_order_detail.count) * product.price
                        user_order_detail.save()
                        return JsonResponse({'status': 200})
                    else:
                        order_detail = OrderDetail.objects.create(count=count, product_id=product.id,
                                                                  order_id=user_order[0].id,
                                                                  final_price=float(product.price) * float(count))
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
    context = {'user_order': user_order.details.exclude(is_active=False).all(), 'total': user_order.get_final_price(), }
    return render(request, 'Eshop_Order/user_bascket.html', context)


@login_required
def remove_item_content(request):
    user_order, created = Order.objects.prefetch_related('details').get_or_create(user_id=request.user.id,
                                                                                  is_active=True, is_paid=False)
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({'status': 'سبد پیدا نشد'})
    else:
        detail = user_order.details.filter(id=detail_id, is_active=True, order__is_active=True, order__is_paid=False,
                                           order__user_id=request.user.id).first()
        if detail is None:
            return JsonResponse({'status': 'سبد پیدا نشد '})
        else:
            detail.is_active = False
            detail.save()
    context = {'user_order': user_order.details.exclude(is_active=False).all(), 'total': user_order.get_final_price(), }

    data = render_to_string('Eshop_Order/user_backet_for_ajax.html', context)
    return JsonResponse({'status': 200, 'data': data})


@login_required
def ChangeOrderCount(request):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({'status': 'محصول پیدا نشد'})

    detail: OrderDetail = OrderDetail.objects.filter(id=detail_id, is_active=True, order__is_active=True,
                                                     order__is_paid=False, order__user_id=request.user.id).first()

    if detail is None:
        return JsonResponse({'status': 'سبد پیدا نشد'})

    if state == 'i':
        detail.count += 1
        detail.final_price = float(detail.count) * float(detail.product.price)
        detail.save()
    elif state == 'd':
        if detail.count <= 1:
            detail.is_active = False
            detail.save()
        elif detail.count > 1:
            detail.count -= 1
            detail.final_price = float(detail.count) * float(detail.product.price)
            detail.save()
        else:
            return JsonResponse({'status': 'مشکلی پیش اومد'})
    else:
        return JsonResponse({'status': 'یافت نشد'})

    user_order, created = Order.objects.prefetch_related('details').get_or_create(user_id=request.user.id,
                                                                                  is_active=True, is_paid=False)

    context = {'user_order': user_order.details.exclude(is_active=False).all(), 'total': user_order.get_final_price(), }
    data = render_to_string('Eshop_Order/user_backet_for_ajax.html', context)
    return JsonResponse({'status': 200, 'data': data})


# ? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/order/verify_payment/'


@login_required
def request_payment(request):
    user_order = Order.objects.get_or_create(user_id=request.user.id, is_active=True, is_paid=False)[0]
    total_price = user_order.get_final_price()
    if total_price <= 0:
        return redirect(reverse('Orders.page'))
    else: return redirect(reverse('verify.payment'))
    # data = {"MerchantID": settings.MERCHANT,
    #         "Amount": total_price * 10,
    #         "Description": description,
    #         "CallbackURL": CallbackURL, }
    # data = json.dumps(data)
    # headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    # try:
    #     response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
    #     if response.status_code == 200:
    #         response = response.json()
    #         if response['Status'] == 100:
    #             return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
    #                     'authority': response['Authority']}
    #         else:
    #             return {'status': False, 'code': str(response['Status'])}
    #     return response
    # except requests.exceptions.Timeout:
    #     return {'status': False, 'code': 'timeout'}
    #
    # except requests.exceptions.ConnectionError:
    #     return {'status': False, 'code': 'connection error'}


@login_required
def verify_payment(request):
    user_order = Order.objects.filter(user_id=request.user.id, is_active=True, is_paid=False).first()
    if user_order is None:
        return redirect(reverse('Orders.page'))
    total_price = user_order.get_final_price()
    if total_price <= 0:
        raise Http404('مشکلی پیش امده است')

    user_order.is_paid = True
    user_order.payment_date = datetime.date.today()
    user_order.save()
    return render(request, 'Eshop_Order/success_payment.html')
    # data = {"MerchantID": settings.MERCHANT,
    #         "Amount": total_price * 10,
    #         "Authority": request.GET.get('authority')
    #         }
    # data = json.dumps(data)
    # headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    # response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
    # if response.status_code == 200:
    #     response = response.json()
    #     if response['Status'] == 100:
    #         return {'status': True, 'RefID': response['RefID']}
    #     else:
    #         return {'status': False, 'code': str(response['Status'])}
    # return response
