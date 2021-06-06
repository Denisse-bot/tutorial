import os
from django.shortcuts import redirect
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.http.response import HttpResponseRedirect
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def send_mail_reserva(atencion):
    

    correo_administrador = os.environ.get('EMAIL_HOST_USER')
    # hora = atencion
    # email = atencion.reserva.email
    # box = atencion.box
    # paciente = atencion.reserva.usuario.nombre
    print(correo_administrador)

    subject = 'Confirmación de reserva'
    template = get_template('core/correo.html')
    content = template.render({'atencion': atencion})
    message = EmailMultiAlternatives(
        subject,
        'Reserva de atención confirmada',
        correo_administrador,
        ['denisse.lyon@gmail.com']
    )
    message.attach_alternative(content, 'text/html')
    message.send()
    return HttpResponseRedirect('listar_atenciones')


##ToDo revisar variable de entorno de correo