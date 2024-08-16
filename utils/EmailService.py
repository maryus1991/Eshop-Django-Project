from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def SendMail(to, subject, context, template_name):
    print('okkkkkk')
    try:
        html_message = render_to_string(template_name, context)
        print('okkkkkk')
        plain_message = strip_tags(html_message)
        print('okkkkkk')
        from_email = settings.EMAIL_HOST_USER
        print('okkkkkk')
        send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        print('okkkkkk')
        return True
    except:
        print('-okkkkkk')
        return False