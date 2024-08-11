from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from .forms import ContactUsForm


def home_index(request):
    return render(request, 'Eshop_home/Eshop_home_index.html')


def contact_page(request):
    return render(request, 'Eshop_home/Eshop_home_Contact-Us.html',
                  {'contact_form': ContactUsForm()})


class contact_page_views(CreateView):
    form_class = ContactUsForm
    template_name = 'Eshop_home/Eshop_home_Contact-Us.html'
    success_url = reverse_lazy('contact.us.page')


def Site_Header_Partial(request):
    return render(request, 'Base/HeaderBase.html')


def Site_Footer_Partial(request):
    return render(request, 'Base/FooterBase.html')
