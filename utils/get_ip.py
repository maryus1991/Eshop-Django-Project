def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        x_forwarded_for = x_forwarded_for.split(',')[0]
    else:
        x_forwarded_for = request.META.get('REMOTE_ADDR')
    return x_forwarded_for
