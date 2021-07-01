from core.models import Atencion, Reserva
import os
from django.shortcuts import redirect
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.http.response import HttpResponseRedirect
from dotenv import load_dotenv, find_dotenv
from django.template.loader import render_to_string

load_dotenv(find_dotenv())

def send_mail_reserva(atencion, id):
    atenciones = Atencion.objects.get(id=id)
    reserva = atenciones.reserva.dia_reservado
    email = atenciones.reserva.usuario.email
    nombre = atenciones.reserva.usuario.nombre
    apellido = atenciones.reserva.usuario.apellido
    box = atenciones.box.id
    especialidad = atenciones.reserva.especialidad
    profesional_nombre= atenciones.especialista.nombre,
    profesional_apellido = atenciones.especialista.apellido,
    centro = atenciones.reserva.sucursal




    subject, from_mail, to = 'Confirmación Reserva Atención Médica','support@Abae.cl' ,email
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
        logger.error(ex)


  
    # subject = 'Confirmación de reserva'
    # template = get_template('core/correo.html')
    # content = template.render({'atencion': atencion})
    # message = EmailMultiAlternatives(
    #     subject,
    #     'Reserva de atención confirmada',
    #     correo_administrador,
    #     ['denisse.lyon@gmail.com']
    # )
    # message.attach_alternative(content, 'text/html')
    # message.send()
    # return HttpResponseRedirect('listar_atenciones')


##ToDo revisar variable de entorno de correo