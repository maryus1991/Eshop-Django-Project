from django import forms
from .models import Eshop_Contact_Us


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = Eshop_Contact_Us
        fields = ['full_name', 'email', 'title', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام'
            }), 'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیـل'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'موضـوع'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'پیغـام شمـا',
                'id': 'message'})
        }

    # name = forms.CharField(label='Full Name',
    #                        widget=forms.TextInput(attrs={
    #                            'class': 'form-control',
    #                            'placeholder': 'نام'
    #
    #                        }))
    # email = forms.EmailField(label='Email Address',
    #                          widget=forms.TextInput(attrs={
    #                              'class': 'form-control',
    #                              'placeholder': 'ایمیـل'
    #                          }))
    # subject = forms.CharField(label='Title',
    #                           widget=forms.TextInput(attrs={
    #                               'class': 'form-control',
    #                               'placeholder': 'موضـوع'
    #                           }))
    # message = forms.CharField(widget=forms.Textarea(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'پیغـام شمـا',
    #     'id': 'message'
    # }))
