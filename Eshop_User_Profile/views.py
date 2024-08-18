from django.contrib.auth import logout
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, View

from Eshop_Account.models import User
from .forms import UserEditForm, UserChangePass


class UserDashBord(TemplateView):
    template_name = 'Eshop_User_Profile/UserDashBord.html'


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


def user_panel_partial(request, user):
    return render(request, 'Eshop_User_Profile/partial/user_panel_partial.html', {'user': user})
