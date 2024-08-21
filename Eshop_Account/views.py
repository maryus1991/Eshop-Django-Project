from django.contrib.auth import login, logout
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View

from Eshop_Account.forms import RegisterForm, LoginForm, ForgotPassFormEmail, ResetPassForm
from utils.EmailService import SendMail
from .models import User


# @login_required
def logout_user(request):
    logout(request)
    return redirect(reverse('login.auth.page'))


class ForgotPass(View):
    def get(self, request):
        forgot_form = ForgotPassFormEmail()
        con = {'forgot_form': forgot_form}
        return render(request, 'Eshop_Account/forget_password.html', con)

    def post(self, request):
        forgot_form = ForgotPassFormEmail(request.POST)
        if forgot_form.is_valid():
            # mobile = forgot_form.cleaned_data.get('phone')
            email = forgot_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=email).first()
            if user is not None:
                status = SendMail(user.email, 'تغییر رمز عبور', {'user': user}, 'emails/forgot_pass.html')
                if status:
                    return redirect(
                        reverse('login.auth.page') + '?status=یک ایمل برای شما ارسال شد لطفا پوشه اپم هارا  هم چک کنید')
                else:
                    raise Http404('مشکلی پیش امده است لطفا دوباره امتحان کنید')
            else:
                forgot_form.add_error('email', 'کاربر یافت نشد')

        return render(request, 'Eshop_Account/forget_password.html')


class ResetPassEmail(View):
    def get(self, request, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('login.auth.page') + '?status=این کلید جاری منقضی شده است')
        else:
            Reset_Pass_Form = ResetPassForm()
            context = {'Reset_Pass_Form': Reset_Pass_Form, 'user': user}
        return render(request, 'Eshop_Account/change_pass.html', context)

    def post(self, request, active_code):
        Reset_Pass_Form = ResetPassForm(request.POST)
        context = {'Reset_Pass_Form': Reset_Pass_Form}
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if Reset_Pass_Form.is_valid():
            if user is not None:
                user.set_password(Reset_Pass_Form.cleaned_data.get('password'))
                user.email_active_code = get_random_string(72)
                user.is_active = True
                user.save()
                return redirect(reverse('login.auth.page') + '?status=رمز عبور شما با موفقیت تغییر داد شد')
            else:
                return Http404('کاربر یافت نشد')
        else:
            raise Http404('کاربر یافت نشد')


# @method_decorator(login_required, name='dispatch')
class RegisterView(View):

    def get(self, request):
        register_form = RegisterForm()
        context = {'register_form': register_form}
        return render(request, 'Eshop_Account/signin.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            email = register_form.cleaned_data.get('email')
            phone = register_form.cleaned_data.get('phone')
            password = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(
                Q(username__iexact=username) | Q(email__iexact=email) | Q(email__iexact=phone)).exists()
            if user:
                register_form.add_error('username', 'این مشخصات قبلا وارد سایت شده است')
            else:
                new_user = User(username=username, email=email, mobile=phone, email_active_code=get_random_string(72),
                                mobile_active_code=get_random_string(10), is_active=False)
                new_user.set_password(password)
                new_user.save()
                SendMail(new_user.email, 'فعال سازی حساب کاربری', {'user': new_user}, 'emails/active.html')
                return redirect(reverse(
                    'login.auth.page') + '?status=لطفا ایمیل را تایید کنید و پوشه اسپم یا هرزنام را هم چک کنید ')
        context = {'register_form': register_form}
        return render(request, 'Eshop_Account/signin.html', context)


# @method_decorator(login_required, name='dispatch')
class loginView(View):
    def get(self, request):
        login_form = LoginForm
        status = request.GET.get('status') or None
        context = {'login_form': login_form, 'status': status}
        return render(request, 'Eshop_Account/login.html', context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user: User = User.objects.filter(username__iexact=login_form.cleaned_data.get('username')).first()
            if user is not None:
                if user.is_active:
                    if user.check_password(login_form.cleaned_data.get('password')):
                        login(request, user)
                        return redirect(reverse('UserDashBord_editUser_Profile_page'))
                    else:
                        login_form.add_error('username', 'کاربر یافت نشد')
                else:
                    login_form.add_error('username', 'کاربر فعال نیست')
            else:
                login_form.add_error('username', 'کاربر یافت نشد')
        context = {'login_form': login_form}
        return render(request, 'Eshop_Account/login.html', context)


# @method_decorator(login_required, name='dispatch')
class activate_account_email(View):
    def get(self, request, activate_account_email):
        try:
            user: User = User.objects.filter(email_active_code__iexact=activate_account_email).first()
            if user is not None:
                user.email_verified = True
                user.is_active = True
                user.is_verified = True
                user.email_active_code = get_random_string(72)
                user.save()
                return redirect(reverse('login.auth.page') + '?status=حساب شما با موفقیت تایید شد ')
            else:
                raise Http404('کاربر پیدا نشد')
        except:
            raise Http404('کاربر پیدا نشد')
