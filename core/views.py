import django
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.core.files.base import ContentFile
from django.db.models.fields import AutoField
from django.core.exceptions import ObjectDoesNotExist
from django.http import request
from django.http.response import HttpResponseRedirect
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from core import models
import core
from django.db.models import Q
from core.models import Atencion, Box, Reserva, Usuario
from core.forms import AtencionForm, UsuarioForm
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from django.urls import reverse_lazy
from .forms import ReservaForm, UsuarioForm

from .forms import BoxesForm, FormularioLogin, ReservaForm, UsuarioForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from .mixins import SuperUsuarioMixin

# Create your views here.


class VistaEnfermera(SuperUsuarioMixin,TemplateView):
    template_name = 'core/vista_enfermera.html'
  
class VistaUsuario(TemplateView):
    template_name = 'core/vista_usuario.html'

class Login(FormView):
    template_name = 'core/login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('vista_enfermera')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request,*args,**kwargs)

    def form_valid(self,form):
        login(self.request,form.get_user())
        return super(Login,self).form_valid(form)
    
def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('login')

class home(TemplateView):
    template_name = 'core/home.html'

class robotos(TemplateView):
    template_name = 'core/robotos.html'


def crearUsuario(request):
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        if usuario_form.is_valid():
            usuario_form.save()
            return redirect('login')
    else:
        usuario_form = UsuarioForm()
    return render(request,'core/crear_usuario.html',{'usuario_form':usuario_form})

def listadoUsuarios(request):
    usuarios = Usuario.objects.all()
    queryset = request.GET.get("search")
    if queryset:
        usuarios = Usuario.objects.filter(
            Q(email__icontains = queryset) |Q(nombre__icontains = queryset)|Q(apellido__icontains = queryset)|Q(rut__icontains = queryset)|Q(comuna__icontains = queryset)
        ).distinct()
    paginator=Paginator(usuarios,3)
    page=request.GET.get('page')
    usuarios = paginator.get_page(page)
    return render(request,'core/listar_usuarios.html',{'usuarios':usuarios})


# def listarUsuario(request):
#     #acá se filtran los usuarios activos o habilitados.
#     usuarios = Usuario.objects.filter(usuario_activo=True)
#     # usuarios = Usuario.objects.all // así se listan todos
#     return render(request, 'core/listar_usuarios.html',{'usuarios':usuarios})

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

    return render(request, 'core/modificar_usuario.html',{'usuario_form':usuario_form,'error':error})


def editar_self_usuario(request):
    id = None
    id = request.user.id
    usuario = Usuario.objects.get(id=id)
    print(usuario)

    if request.method == 'GET':
        usuario_form = UsuarioForm(instance=usuario)
        print(usuario_form)
    else:
        usuario_form = UsuarioForm(request.POST, instance=usuario)
        if usuario_form.is_valid():
            usuario_form.save()
            print(usuario_form)
        return redirect('listar_usuarios')

    return render(request,'core/modificar_usuario.html',{'usuario_form':usuario_form})


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
    usuario = request.user
    if request.method == 'POST':
        if not request.POST._mutable:
            request.POST._mutable = True
            # forma de acceder y modificar el diccionario para el formulario 
            request.POST['usuario'] = request.user
            print(request.POST)
            reserva_form = ReservaForm(request.POST)
            if reserva_form.is_valid():
                print(reserva_form)
                reserva_form.save()
                
                return redirect('listar_reservas_self')
    else:
        reserva_form = ReservaForm()
    return render(request,'core/crear_reserva.html',{'reserva_form':reserva_form, 'usuario':usuario})


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


def crearBox(request):
    if request.method == 'POST':
        boxes_form = BoxesForm(request.POST)
        if boxes_form.is_valid():
            boxes_form.save()
            return redirect('listar_boxes')
    else:
        boxes_form = BoxesForm()
    return render(request,'core/crear_box.html',{'boxes_form':boxes_form})


def editarBox(request, id):
    box = Box.objects.get(id=id)
    if request.method =='GET':
        boxes_form = BoxesForm(instance=box)
    else:
        boxes_form = BoxesForm(request.POST, instance=box)
        if boxes_form.is_valid():
            boxes_form.save()
        return redirect('listar_boxes')
    return render(request, 'core/crear_box.html', {'boxes_form': boxes_form})

def eliminarBox(request,id):
    box = Box.objects.get(id=id)
    if request.method == 'POST':
        box.save()
        box.delete()
        return redirect('listar_boxes')
    return render(request,'core/eliminar_box.html', {'box':box})

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

def listadoReservasSelf(request):
    id = request.user.id
    queryset = request.GET.get("search")
    print(id)
    reservas = Reserva.objects.filter(usuario=id)
    if queryset:
        reservas = Reserva.objects.filter(
            Q(dia_reservado__icontains = queryset)
        ).distinct()
    paginator=Paginator(reservas,2)
    page=request.GET.get('page')
    reservas = paginator.get_page(page)
    return render(request,'core/listar_mis_reservas.html',{'reservas':reservas})


def listadoReservas(request):
    queryset = request.GET.get("search")
    reservas = Reserva.objects.all()
    if queryset:
        reservas = Reserva.objects.filter(
            Q(dia_reservado__icontains = queryset) |Q(usuario__icontains = queryset)
        ).distinct()
    paginator=Paginator(reservas,2)
    page=request.GET.get('page')
    reservas = paginator.get_page(page)
    return render(request,'core/listar_reservas.html',{'reservas':reservas})

# class listadoReservas(ListView):
#     model = Reserva
#     template_name = 'core/listar_reservas.html'
#     context_object_name = 'reservas'
#     queryset = Reserva.objects.all()


# class listadoUsuarios(ListView):
#     model = Usuario
#     template_name = 'core/listar_usuarios.html'
#     context_object_name = 'usuarios'
#     queryset = Usuario.objects.all()


def listadoBoxes(request):
    queryset = request.GET.get("search")
    boxes = Box.objects.all()
    if queryset:
        boxes = Box.objects.filter(
            Q(estado__icontains = queryset) |Q(especialidad__icontains = queryset)
        ).distinct()

    paginator=Paginator(boxes,2)
    page=request.GET.get('page')
    boxes = paginator.get_page(page)
    return render(request,'core/listar_boxes.html',{'boxes':boxes})
# class listadoBoxes(ListView):
#     model = Box
#     template_name = 'core/listar_boxes.html'
#     context_object_name = 'boxes'
#     queryset = Box.objects.all()

def listadoAtenciones(request):
    queryset = request.GET.get("search")
    atenciones = Atencion.objects.all()
    if queryset:
        atenciones = Atencion.objects.filter(
            Q(nombre_especialista__icontains = queryset) |Q(apellido_especialista__icontains = queryset) |Q(box__exact = queryset)
        ).distinct()

    paginator=Paginator(atenciones,2)
    page=request.GET.get('page')
    atenciones = paginator.get_page(page)
    return render(request,'core/listar_atenciones.html',{'atenciones':atenciones})

# class listadoAtenciones(ListView):
#     model = Atencion
#     template_name = 'core/listar_atenciones.html'
#     context_object_name = 'atenciones' #es el nombre por el que se llamará el conjunto de objetos en el template(html)
#     queryset = Atencion.objects.all()

class actualizarAtencion(UpdateView):
    model = Atencion
    template_name = 'core/crear_atencion.html'
    form_class = AtencionForm
    success_url = reverse_lazy('core:listar_atenciones')

def insumo(request):
    from django.db import connection
    with connection.cursor() as cursor:
        #cursor.execute("SELECT ID_INSUMO,NOMBRE_INSUMO,ESPECIALIDAD,STOCK FROM INSUMO") vista original
        cursor.execute("SELECT ID,NOMBRE,ESPECIALIDAD,STOCK FROM INSUMO")
        rawData = cursor.fetchall()
        result = []
        for r in rawData:
            result.append(list(r))
        contexto = {'consultas': result }
    return render(request, 'core/insumo.html', contexto)         
