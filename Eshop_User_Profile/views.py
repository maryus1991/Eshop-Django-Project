from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View, ListView

from Eshop_Account.models import User
from Eshop_Order.models import Order
from .forms import UserEditForm, UserChangePass


@method_decorator(login_required, name='dispatch')
class UserDashBord_editUser_Profile_page(View):
    def get(self, request, *args, **kwargs):
        curren_user = User.objects.filter(id=request.user.id, is_active=True, is_deleted=False).first()
        context = {'UsereditForm': UserEditForm(instance=curren_user), 'user': curren_user}
        return render(request, 'Eshop_User_Profile/UserDashBord.html', context)

    def post(self, request, *args, **kwargs):
        curren_user = User.objects.filter(id=request.user.id, is_active=True, is_deleted=False).first()
        edit_form = UserEditForm(request.POST, request.FILES, instance=curren_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)
        context = {'UsereditForm': edit_form, 'user': curren_user}
        return render(request, 'Eshop_User_Profile/UserDashBord.html', context)


@method_decorator(login_required, name='dispatch')
class UserDashBord_Change_pass(TemplateView):
    template_name = 'Eshop_User_Profile/UserDashBordChangePass.html'

    def get(self, request, *args, **kwargs):
        context = {'UserChangePass': UserChangePass()}
        return render(request, 'Eshop_User_Profile/UserDashBordChangePass.html', context)

    def post(self, request, *args, **kwargs):
        form = UserChangePass(request.POST)
        print('okkkk')
        if form.is_valid():
            print('okkkk')
            user: User = User.objects.filter(id=request.user.id, is_active=True, is_deleted=False).first()
            if user.check_password(form.cleaned_data.get('current_pass')):
                print('okkkk')
                user.set_password(form.cleaned_data.get('password'))
                user.save()
                logout(request)
                return redirect(reverse('login.auth.page'))
            else:
                form.add_error('', 'رمز اشتباه است')

        context = {'UserChangePass': form}
        return render(request, 'Eshop_User_Profile/UserDashBordChangePass.html', context)


@method_decorator(login_required, name='dispatch')
class user_shopping_history(ListView):
    model = Order
    template_name = 'Eshop_User_Profile/UserShoppingHistory.html'
    context_object_name = 'orders'

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(user_id=self.request.user.id, is_paid=True, is_active=True)
        return query


@login_required
def user_panel_partial(request, user):
    return render(request, 'Eshop_User_Profile/partial/user_panel_partial.html', {'user': user})


@login_required
def order_detail(request, oid):
    order:Order = Order.objects.prefetch_related('details').filter(user_id=request.user.id, id=oid, is_active=True).first()
    if order is None:
        raise Http404('سبد خرید مورد نظر یافت نشد')
    context = {
        'order_details': order.details.filter(is_active=True).all()
    }
    return render(request, 'Eshop_User_Profile/UserOrderShoppingHistory.html', context)
