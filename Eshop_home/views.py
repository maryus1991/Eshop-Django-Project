from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Eshop_Contact_Us
from .forms import ContactUsForm

def home_index(request):
    return render(request, 'Eshop_home/Eshop_home_index.html')


def contact_page(request):
    return render(request, 'Eshop_home/Eshop_home_Contact-Us.html',
                  {'contact_form': ContactUsForm()}
                  )


def add_Eshop_Contact_Us(request):
    if request.method == 'POST':
        contact_form = ContactUsForm(request.POST)
        contact_form.is_valid()
        if contact_form.is_valid():
            Eshop_Contact_Us.objects.create(full_name=contact_form.cleaned_data['name'],
                                            email=contact_form.cleaned_data['email'],
                                            title=contact_form.cleaned_data['subject'],
                                            message=contact_form.cleaned_data['message'])
            return redirect(reverse('home.index.page'))
        else:
            return render(request, 'Eshop_home/Eshop_home_Contact-Us.html', {'contact_form': contact_form})


def Site_Header_Partial(request):
    return render(request, 'Base/HeaderBase.html')


def Site_Footer_Partial(request):
    return render(request, 'Base/FooterBase.html')

