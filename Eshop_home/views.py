from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Eshop_Slider
from Eshop_Setting.models import SiteSettings
from .forms import ContactUsForm


def home_index(request):
    context = {
        'slider' : Eshop_Slider.objects.filter(is_active=True, is_delete=False).all()[:2],
        'SiteSettings': SiteSettings.objects.filter(is_main_setting=True, is_active=True).first()
    }

    return render(request, 'Eshop_home/Eshop_home_index.html', context)


def About_page(request):
    # site_settings =
    context = {
        'SiteSettings': SiteSettings.objects.filter(is_main_setting=True, is_active=True).first()
    }
    return render(request, 'Eshop_home/About.html', context)



class contact_page_views(CreateView):
    form_class = ContactUsForm
    template_name = 'Eshop_home/Eshop_home_Contact-Us.html'
    success_url = reverse_lazy('contact.us.page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['SiteSettings'] = SiteSettings.objects.filter(is_main_setting=True, is_active=True).first()
        return context


def Site_Header_Partial(request):
    context = {'SiteSettings': SiteSettings.objects.filter(is_main_setting=True, is_active=True).first()}
    return render(request, 'Base/HeaderBase.html', context)


def Site_Footer_Partial(request):
    context = {'SiteSettings': SiteSettings.objects.filter(is_main_setting=True, is_active=True).first()}
    return render(request, 'Base/FooterBase.html', context)
