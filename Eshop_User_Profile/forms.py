from django import forms
from django.core.exceptions import ValidationError

from Eshop_Account.models import User


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'last_name', 'about_user', 'avatar']
        widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}),
                   'about_user': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'درباره شما'}),
                   'avatar': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'عکس پروفایل'}), }

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        avatar.name = str(avatar.name).replace(' ', '')
        return avatar


class UserChangePass(forms.Form):
    current_pass = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'رمز فعلی'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'رمز جدید'
        }
    ))
    conform_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': ' تایید رمز جدید'
        }
    ))

    def clean_conform_password(self):
        password = self.cleaned_data.get('password')
        conform_password = self.cleaned_data.get('conform_password')
        if password == conform_password:
            return conform_password
        else:
            raise ValidationError('کلمه عبور و تکرار ان غیر هم سان هستند')
