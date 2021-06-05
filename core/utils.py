from django.shortcuts import redirect
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.http.response import HttpResponseRedirect



def send_mail_reserva(atencion):
    
    subject = 'confirmación de reserva'
    template = get_template('core/correo.html')
    content = template.render({'atencion': atencion})
    message = EmailMultiAlternatives(
        subject,#titulo
        ''"",
        'chispamelodeath@gmail.com',
        ['denisse.lyon@gmail.com']
    )
    message.attach_alternative(content, 'text/html')
    message.send()
    return HttpResponseRedirect('listar_atenciones')

