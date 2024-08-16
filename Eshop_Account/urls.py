from django.urls import path
from .views import RegisterView, loginView, activate_account_email, ForgotPass, ResetPassEmail, logout_user

urlpatterns = [
    path('regester', RegisterView.as_view(), name='register.auth.page'),
    path('login', loginView.as_view(), name='login.auth.page'),
    path('logout', logout_user, name='logout.auth.page'),
    path('forgutpassword', ForgotPass.as_view(), name='forgot.pass.auth.page'),
    path('reset-pass/email/<str:active_code>', ResetPassEmail.as_view(), name='reset.pass.auth.page.2.3'),
    path('activate-account/email/<activate_account_email>', activate_account_email.as_view(), name='activate.email.auth.page'),
]