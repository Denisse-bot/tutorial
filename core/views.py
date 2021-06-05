import django
from django.db.models.fields import AutoField
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from core import models
import core
from core.models import Atencion, Reserva, Usuario
from core.forms import AtencionForm, UsuarioForm
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from django.urls import reverse_lazy
from .forms import ReservaForm, UsuarioForm
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


# Create your views here.
class home(TemplateView):
    template_name = 'core/home.html'

class robotos(TemplateView):
    template_name = 'core/robotos.html'


def crearUsuario(request):
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        if usuario_form.is_valid():
            usuario_form.save()
            return redirect('listar_usuarios')
    else:
        usuario_form = UsuarioForm()
    return render(request,'core/crear_usuario.html',{'usuario_form':usuario_form})

def listarUsuario(request):
    #acá se filtran los usuarios activos o habilitados.
    usuarios = Usuario.objects.filter(usuario_activo=True)

    # usuarios = Usuario.objects.all // así se listan todos
    return render(request, 'core/listar_usuarios.html',{'usuarios':usuarios})

def editarUsuario(request,id):
    usuario_form = None
    error = None
    try:
        usuario = Usuario.objects.get(id = id)
        if request.method == 'GET':
            usuario_form = UsuarioForm(instance=usuario)
        else:
            usuario_form = UsuarioForm(request.POST, instance=usuario)
            if usuario_form.is_valid():
                usuario_form.save()
            return redirect('listar_usuarios')
    except ObjectDoesNotExist as e:
        error = e

    return render(request, 'core/crear_usuario.html',{'usuario_form':usuario_form,'error':error})


def eliminarUsuario(request,id):
    usuario = Usuario.objects.get(id = id)
    if request.method == 'POST':
        #deshabilitamos el usuario
        #usuario.usuario_activo = False
        usuario.save()
        usuario.delete() # de esta forma se elimina fisicamente el registro
        return redirect('listar_usuarios')
    return render(request, 'core/eliminar_usuario.html',{'usuario':usuario})

def crearReserva(request):
    if request.method == 'POST':
        reserva_form = ReservaForm(request.POST)
        if reserva_form.is_valid():
            reserva_form.save()
            return redirect('listar_reservas')
    else:
        reserva_form = ReservaForm()
    return render(request,'core/crear_reserva.html',{'reserva_form':reserva_form})

def editarReserva(request,id):
    reserva = Reserva.objects.get(id = id)
    if request.method == 'GET':
        reserva_form = ReservaForm(instance=reserva)
    else:
        reserva_form = ReservaForm(request.POST, instance=reserva)
        if reserva_form.is_valid():
            reserva_form.save()
        return redirect('listar_reservas')
    return render(request,'core/crear_reserva.html',{'reserva_form':reserva_form})


def eliminarReserva(request,id):
    reserva = Reserva.objects.get(id = id)
    if request.method == 'POST':
        #deshabilitamos el usuario
        #usuario.usuario_activo = False
        reserva.save()
        reserva.delete() # de esta forma se elimina fisicamente el registro
        return redirect('listar_reservas')
    return render(request, 'core/eliminar_reserva.html',{'reserva':reserva})


def crearAtencion(request):
    if request.method == 'POST':
        atencion_form = AtencionForm(request.POST)
        if atencion_form.is_valid():
            atencion_form.save()
            return redirect('listar_atenciones')
    else:
        atencion_form = AtencionForm()
    return render(request,'core/crear_atencion.html',{'atencion_form':atencion_form})

def editarAtencion(request,id):
    atencion = Atencion.objects.get(id = id)
    if request.method == 'GET':
        atencion_form = AtencionForm(instance=atencion)
    else:
        atencion_form = AtencionForm(request.POST, instance=atencion)
        if atencion_form.is_valid():
            atencion_form.save()
        return redirect('listar_atenciones')
    return render(request,'core/crear_atencion.html',{'atencion_form':atencion_form})

def eliminarAtencion(request,id):
    atencion = Atencion.objects.get(id = id)
    if request.method == 'POST':
        #deshabilitamos el usuario
        #usuario.usuario_activo = False
        atencion.save()
        atencion.delete() # de esta forma se elimina fisicamente el registro
        return redirect('listar_atenciones')
    return render(request, 'core/eliminar_atencion.html',{'atencion':atencion})

def send_email(mail):

    context = {'mail': mail}

    template = get_template('correo.html')
    content = template.render(context)

    email = EmailMultiAlternatives(
        'Correo de ejemplo',
        'Robotos',
        settings.EMAIL_HOST_USER,
        [mail],
    )

    email.attach_alternative(content, 'text/html')
    email.send()


def index(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')

        send_email(mail)

    return render(request, 'index.html',{})   

class listadoReservas(ListView):
    model = Reserva
    template_name = 'core/listar_reservas.html'
    context_object_name = 'reservas'
    queryset = Reserva.objects.all()


class listadoUsuarios(ListView):
    model = Usuario
    template_name = 'core/listar_usuarios.html'
    context_object_name = 'usuarios'
    queryset = Usuario.objects.all()



class listadoAtenciones(ListView):
    model = Atencion
    template_name = 'core/listar_atenciones.html'
    context_object_name = 'atenciones' #es el nombre por el que se llamará el conjunto de objetos en el template(html)
    queryset = Atencion.objects.all()

class actualizarAtencion(UpdateView):
    model = Atencion
    template_name = 'core/crear_atencion.html'
    form_class = AtencionForm
    success_url = reverse_lazy('core:listar_atenciones')


