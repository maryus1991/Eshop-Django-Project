from django import forms


class ContactUsForm(forms.Form):
    name = forms.CharField(label='Full Name',
                           widget=forms.TextInput(attrs={
                               'class': 'form-control',
                               'placeholder': 'نام'

                           }))
    email = forms.EmailField(label='Email Address',
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                                 'placeholder': 'ایمیـل'
                             }))
    subject = forms.CharField(label='Title',
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control',
                                  'placeholder': 'موضـوع'
                              }))
    message = forms.CharField(widget=forms.Textarea(attrs={
                                  'class': 'form-control',
                                  'placeholder': 'پیغـام شمـا',
                                  'id': 'message'
                              }))

