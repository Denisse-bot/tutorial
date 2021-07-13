from os import name
from django.urls import path
from .views import * 
from .utils import send_mail_reserva


urlpatterns = [
    path('', home.as_view(), name = 'home'),
    path('robotos', robotos.as_view(), name='robotos'),
    path('send_mail_reserva/<int:id>', send_mail_reserva, name= 'send_mail_reserva'),
    path('vista_enfermera/', VistaEnfermera.as_view(),name='vista_enfermera'),
    path('vista_funcionario/',VistaFuncionario.as_view(),name='vista_funcionario'),
    path('vista_usuario/', VistaUsuario.as_view(),name='vista_usuario'),
    path('insumo/',insumo, name='insumo'),

    path('crear_funcionario/',crearFuncionario,name='crear_funcionario'),
    path('listar_funcionarios/',listadoFuncionarios,name='listar_funcionarios'),
    path('filtrar_especialidad1',filtrar_especialidad1,name='filtrar_especialidad1'),
    path('filtrar_especialidad2',filtrar_especialidad2,name='filtrar_especialidad2'),
    path('filtrar_especialidad3',filtrar_especialidad3,name='filtrar_especialidad3'),
    path('editar_self_funcionario',editar_self_funcionario,name='editar_self_funcionario'),    

    path('crear_usuario/',crearUsuario,name='crear_usuario'),
    path('listar_pacientes/',listadoPacientes,name='listar_pacientes'),
    path('filtrar_etapa1/',filtradoPacientes1,name='filtrar_etapa1'),
    path('filtrar_etapa2/',filtradoPacientes2,name='filtrar_etapa2'),
    path('filtrar_etapa3/',filtradoPacientes3,name='filtrar_etapa3'),
    path('editar_usuario/<int:id>',editarUsuario,name='editar_usuario'),
    path('editar_self_usuario',editar_self_usuario,name='editar_self_usuario'),    
    path('eliminar_usuario/<int:id>',eliminarUsuario, name = 'eliminar_usuario'),

    path('crear_sucursal/', crearSucursal, name='crear_sucursal'),
    path('listar_sucursales/', listadoSucursales, name='listar_sucursales'),
    path('editar_sucursal/<int:id>', editarSucursal, name='editar_sucursal'),
    path('eliminar_sucursal/<int:id>', eliminarSucursal, name='eliminar_sucursal'),

    path('crear_especialidad/', crearEspecialidad, name='crear_especialidad'),
    path('listar_especialidad/', listadoEspecialidades, name='listar_especialidad'),
    path('editar_especialidad/<int:id>', editarEspecialidad, name='editar_especialidad'),
    path('eliminar_especialidad/<int:id>',eliminarEspecialidad, name='eliminar_especialidad'),

    path('crear_reservas/',crearReserva, name='crear_reservas'),
    #path('crear_reservas_self/',crearReservaSelf, name='crear_reservas_self'),
    path('listar_reservas/',listadoReservas, name='listar_reservas'),
    path('listar_reservas_self/',listadoReservasSelf, name='listar_reservas_self'),
    path('listar_reservas_today/',listadoReservasToday, name='listar_reservas_today'),
    path('listar_reservas_kine/',listadoReservasKine, name='listar_reservas_kine'),
    path('listar_reservas_fono/',listadoReservasFono, name='listar_reservas_fono'),
    path('editar_reserva/<int:id>', editarReserva, name='editar_reserva'),
    path('eliminar_reserva/<int:id>', eliminarReserva, name='eliminar_reserva'),

    path('crear_atencion/<int:id>/<str:especialidad>/<str:sucursal>',crearAtencion,name='crear_atencion'),
    path('editar_atencion/<int:id>', editarAtencion, name='editar_atencion'),
    path('listar_atenciones/',listadoAtenciones, name='listar_atenciones'),
    path('listar_atenciones_today/',listadoAtencionesToday, name='listar_atenciones_today'),
    path('listar_atenciones_self/',listadoAtencionesSelf, name='listar_atenciones_self'),
    path('listar_atenciones_self_today/',listadoAtencionesSelfToday, name='listar_atenciones_self_today'),
    path('eliminar_atencion/<int:id>',eliminarAtencion, name='eliminar_atencion'),

    path('crear_box/',crearBox, name='crear_box'),
    path('listar_boxes/',listadoBoxes, name='listar_boxes'),
    path('editar_box/<int:id>',editarBox, name='editar_box'),
    path('eliminar_box/<int:id>',eliminarAtencion,name='eliminar_box')

]

