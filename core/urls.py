from django.urls import path
from .views import * 
from .utils import send_mail_reserva
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', home.as_view(), name = 'home'),
    path('robotos', robotos.as_view(), name='robotos'),
    path('send_mail_reserva', send_mail_reserva, name= 'send_mail_reserva'),

    path('crear_usuario/',crearUsuario,name='crear_usuario'),
    path('listar_usuarios/',listadoUsuarios.as_view(),name='listar_usuarios'),
    path('editar_usuario/<int:id>',editarUsuario,name='editar_usuario'),
    path('eliminar_usuario/<int:id>',eliminarUsuario, name = 'eliminar_usuario'),

    path('crear_reservas/',login_required(crearReserva), name='crear_reservas'),
    path('listar_reservas/',listadoReservas.as_view(), name='listar_reservas'),
    path('editar_reserva/<int:id>', editarReserva, name='editar_reserva'),
    path('eliminar_reserva/<int:id>', eliminarReserva, name='eliminar_reserva'),

    path('crear_atencion/',crearAtencion,name='crear_atencion'),
    path('editar_atencion/<int:id>', editarAtencion, name='editar_atencion'),
    path('listar_atenciones/',listadoAtenciones.as_view(), name='listar_atenciones'),
    path('eliminar_atencion/<int:id>',eliminarAtencion, name='eliminar_atencion'),

    path('crear_box/',crearBox, name='crear_box'),
    path('listar_boxes/',listadoBoxes.as_view(), name='listar_boxes'),
    path('editar_box/<int:id>',editarBox, name='editar_box'),
    path('eliminar_box/<int:id>',eliminarAtencion,name='eliminar_box')

]
