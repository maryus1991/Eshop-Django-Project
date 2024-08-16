from django import forms
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    username = forms.CharField(label='نام کاربری'
                               )
    email = forms.EmailField(label='ایمیل'
                             )
    phone = forms.CharField(label='',
                            widget=forms.NumberInput(attrs={'placeholder': 'شماره مبایل',
                                                            }))
    password = forms.CharField(label='',
                               widget=forms.PasswordInput(attrs={'placeholder': 'کلمه عبور',
                                                                 }))
    conform_password = forms.CharField(label='',
                                       widget=forms.PasswordInput(attrs={'placeholder': 'تکرار کلمه عبور',
                                                                         }))

    def clean_conform_password(self):
        password = self.cleaned_data.get('password')
        conform_password = self.cleaned_data.get('conform_password')
        if password == conform_password:
            return conform_password
        else:
            raise ValidationError('کلمه عبور و تکرار ان غیر هم سان هستند')


class LoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری')
    password = forms.CharField(label='',
                               widget=forms.PasswordInput(attrs={'placeholder': 'کلمه عبور',
                                                                 }))


class ForgotPassFormEmail(forms.Form):
    # phone = forms.CharField(label='',
    #                         widget=forms.NumberInput(attrs={'placeholder': 'شماره مبایل',
    #                                                         }))
    email = forms.EmailField(label='ایمیل')


class ResetPassForm(forms.Form):
    password = forms.CharField(label='',
                               widget=forms.PasswordInput(attrs={'placeholder': 'کلمه عبور',
                                                                 }))
    conform_password = forms.CharField(label='',
                                       widget=forms.PasswordInput(attrs={'placeholder': 'تکرار کلمه عبور',
                                                                         }))


    def clean_conform_password(self):
        password = self.cleaned_data.get('password')
        conform_password = self.cleaned_data.get('conform_password')
        if password == conform_password:
            return conform_password
        else:
            raise ValidationError('کلمه عبور و تکرار ان غیر هم سان هستند')
