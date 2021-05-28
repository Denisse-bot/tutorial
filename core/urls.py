from django.urls import path
from .views import crearReserva, editarReserva,eliminarReserva, home, crearUsuario, editarUsuario, listadoUsuarios, eliminarUsuario, listadoReservas, listadoAtenciones,actualizarAtencion, crearAtencion, editarAtencion, eliminarAtencion

urlpatterns = [
    path('', home.as_view(), name = 'home'),

    path('crear_usuario/',crearUsuario,name='crear_usuario'),
    path('listar_usuarios/',listadoUsuarios.as_view(),name='listar_usuarios'),
    path('editar_usuario/<int:id>',editarUsuario,name='editar_usuario'),
    path('eliminar_usuario/<int:id>',eliminarUsuario, name = 'eliminar_usuario'),

    path('crear_reservas/',crearReserva, name='crear_reservas'),
    path('listar_reservas/',listadoReservas.as_view(), name='listar_reservas'),
    path('editar_reserva/<int:id>', editarReserva, name='editar_reserva'),
    path('eliminar_reserva/<int:id>', eliminarReserva, name='eliminar_reserva'),

    path('crear_atencion/',crearAtencion,name='crear_atencion'),
    path('editar_atencion/<int:id>', editarAtencion, name='editar_atencion'),
    path('listar_atenciones/',listadoAtenciones.as_view(), name='listar_atenciones'),
    path('eliminar_atencion/<int:id>',eliminarAtencion, name='eliminar_atencion'),
]
