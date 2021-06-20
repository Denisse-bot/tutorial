from os import name
from django.urls import path
from .views import * 
from .utils import send_mail_reserva


urlpatterns = [
    path('', home.as_view(), name = 'home'),
    path('robotos', robotos.as_view(), name='robotos'),
    path('send_mail_reserva/<int:id>', send_mail_reserva, name= 'send_mail_reserva'),
    path('vista_enfermera/', VistaEnfermera.as_view(),name='vista_enfermera'),
    path('vista_usuario/', VistaUsuario.as_view(),name='vista_usuario'),
    path('insumo/',insumo, name='insumo'),

    path('crear_usuario/',crearUsuario,name='crear_usuario'),
    path('crear_funcionario/',crearFuncionario,name='crear_funcionario'),
    path('listar_usuarios/',listadoUsuarios,name='listar_usuarios'),
    path('editar_usuario/<int:id>',editarUsuario,name='editar_usuario'),
    path('editar_self_usuario',editar_self_usuario,name='editar_self_usuario'),    
    path('eliminar_usuario/<int:id>',eliminarUsuario, name = 'eliminar_usuario'),

    path('crear_sucursal/', crearSucursal, name='crear_sucursal'),
    path('listar_sucursales/', listadoSucursales, name='listar_sucursales'),
    path('editar_sucursal/<int:id>', editarSucursal, name='editar_sucursal'),
    path('eliminar_sucursal/<int:id>', eliminarSucursal, name='eliminar_sucursal'),

    

    path('crear_reservas/',crearReserva, name='crear_reservas'),
    #path('crear_reservas_self/',crearReservaSelf, name='crear_reservas_self'),
    path('listar_reservas/',listadoReservas, name='listar_reservas'),
    path('listar_reservas_self/',listadoReservasSelf, name='listar_reservas_self'),
    path('editar_reserva/<int:id>', editarReserva, name='editar_reserva'),
    path('eliminar_reserva/<int:id>', eliminarReserva, name='eliminar_reserva'),

    path('crear_atencion/',crearAtencion,name='crear_atencion'),
    path('editar_atencion/<int:id>', editarAtencion, name='editar_atencion'),
    path('listar_atenciones/',listadoAtenciones, name='listar_atenciones'),
    path('eliminar_atencion/<int:id>',eliminarAtencion, name='eliminar_atencion'),

    path('crear_box/',crearBox, name='crear_box'),
    path('listar_boxes/',listadoBoxes, name='listar_boxes'),
    path('editar_box/<int:id>',editarBox, name='editar_box'),
    path('eliminar_box/<int:id>',eliminarAtencion,name='eliminar_box')

]

