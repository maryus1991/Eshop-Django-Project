from django.shortcuts import render


def home_index(request):
    return render(request, 'Eshop_home/Eshop_home_index.html')


def contact_page(request):
    return render(request, 'Eshop_home/Eshop_home_Contact-Us.html')


def Site_Header_Partial(request):
    return render(request, 'Base/HeaderBase.html')


def Site_Footer_Partial(request):
    return render(request, 'Base/FooterBase.html')

