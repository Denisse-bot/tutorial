from core.models import Atencion, Reserva
import os
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
from dotenv import load_dotenv, find_dotenv
from django.template.loader import render_to_string
from logging import Logger

load_dotenv(find_dotenv())

EMAIL_HOST_USER_TO = os.environ.get('EMAIL_HOST_USER_TO')

def send_mail_reserva(atencion, id):
    atenciones = Atencion.objects.get(id=id)
    reserva = atenciones.reserva.dia_reservado
    email = atenciones.reserva.usuario.email
    nombre = atenciones.reserva.usuario.nombre
    apellido = atenciones.reserva.usuario.apellido
    box = atenciones.box
    especialidad = atenciones.reserva.especialidad
    profesional_nombre= atenciones.especialista.nombre,
    profesional_apellido = atenciones.especialista.apellido,
    centro = atenciones.reserva.sucursal


    subject, from_mail, to = 'Confirmación Reserva Atención Médica','soporteabae@gmail.com',email
    text_context = '%s Hemos confirmado tu reserva de atención médica.' % nombre
    msg_html = render_to_string('core/correo.html', {
        'nombre': nombre,
        'apellido': apellido,
        'reserva': reserva,
        'profesional_nombre': profesional_nombre,
        'profesional_apellido':profesional_apellido,
        'email': email,
        'especialidad': especialidad,
        'box': box,
        'centro': centro
    })
	
    try:
        msg = EmailMultiAlternatives(subject, text_context, from_mail, [to])
        msg.attach_alternative(msg_html, "text/html")
        msg.send()
        return redirect('listar_atenciones')
    except Exception as ex:
        Logger.error(ex)


def send_mail_notificacion(atencion, id):
    atenciones = Atencion.objects.get(id=id)
    reserva = atenciones.reserva.dia_reservado
    box = atenciones.box
    especialidad = atenciones.reserva.especialidad
    centro = atenciones.reserva.sucursal
    nombre= 'Personal Edudown'
    email = EMAIL_HOST_USER_TO
    
    subject, from_mail, to = 'Confirmación Atención Médica Realizada','soporteabae@gmail.com',email
    text_context = '%s Hemos confirmado la atencion en el box ' % box
    msg_html = render_to_string('core/notificacion_box.html', {
        'nombre': nombre,
        'reserva': reserva,
        'especialidad': especialidad,
        'box': box,
        'centro': centro
    })
    try:
        msg = EmailMultiAlternatives(subject, text_context, from_mail, [to])
        msg.attach_alternative(msg_html, "text/html")
        msg.send()
        return redirect('listar_atenciones_self')
    except Exception as ex:
        Logger.error(ex)
