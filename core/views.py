import django
from datetime import date
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
from core.models import Atencion, Box, Especialidad, Reserva, Sucursal, Usuario, UsuarioManager
from core.forms import AtencionForm, UsuarioForm
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from django.urls import reverse_lazy
from .forms import ReservaForm, UsuarioForm

from .forms import BoxesForm, FormularioLogin, ReservaForm, UsuarioForm, SucursalesForm, EspecialidadForm, ModifyUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from .mixins import SuperUsuarioMixin
from django.utils.timezone import datetime

# Create your views here.


class VistaEnfermera(LoginRequiredMixin,SuperUsuarioMixin,TemplateView):

    template_name = 'core/vista_enfermera.html'
  
class VistaFuncionario(LoginRequiredMixin,TemplateView):
    template_name = 'core/vista_funcionario.html'

class VistaUsuario(LoginRequiredMixin,TemplateView):
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

def crearEspecialidad(request):
    if request.method == 'POST':
        especialidad_form = EspecialidadForm(request.POST)
        print(especialidad_form)
        if especialidad_form.is_valid():
            especialidad_form.save()
            return redirect('listar_especialidad')
    else:
        especialidad_form = EspecialidadForm()
    return render(request,'core/crear_especialidad.html',{'especialidad_form':especialidad_form})

def listadoEspecialidades(request):
    queryset = request.GET.get("search")
    especialidades = Especialidad.objects.all()
    if queryset:
        especialidades = Especialidad.objects.filter(
            Q(nombre__icontains = queryset[0]) |Q(direccion__icontains = queryset)
        ).distinct()

    paginator=Paginator(especialidades,3)
    page=request.GET.get('page')
    especialidades = paginator.get_page(page)
    return render(request,'core/listar_especialidad.html',{'especialidades':especialidades})

def editarEspecialidad(request, id):
    especialidad = Especialidad.objects.get(id=id)
    print(especialidad)
    if request.method =='GET':
        especialidad_form = EspecialidadForm(instance=especialidad)
        print(especialidad_form)
    else:
        especialidad_form = EspecialidadForm(request.POST, instance=especialidad)
        if especialidad_form.is_valid():
            print(especialidad_form)
            especialidad_form.save()
        return redirect('listar_especialidad')
    return render(request, 'core/modificar_especialidad.html', {'especialidad_form': especialidad_form})

def eliminarEspecialidad(request,id):
    especialidad = Especialidad.objects.get(id=id)
    if request.method == 'POST':
        especialidad.save()
        especialidad.delete()
        return redirect('listar_especialidad')
    return render(request,'core/eliminar_especialidad.html', {'especialidad':especialidad})

def crearSucursal(request):
    if request.method == 'POST':
        sucursal_form = SucursalesForm(request.POST)
        print(sucursal_form)
        if sucursal_form.is_valid():
            sucursal_form.save()
            return redirect('listar_sucursales')
    else:
        sucursal_form = SucursalesForm()
        print('tupoto')
    return render(request,'core/crear_sucursal.html',{'sucursal_form':sucursal_form})

def listadoSucursales(request):
    queryset = request.GET.get("search")
    sucursales = Sucursal.objects.all()
    if queryset:
        sucursales = Sucursal.objects.filter(
            Q(nombre__icontains = queryset[0]) |Q(direccion__icontains = queryset)
        ).distinct()

    paginator=Paginator(sucursales,3)
    page=request.GET.get('page')
    sucursales = paginator.get_page(page)
    return render(request,'core/listar_sucursales.html',{'sucursales':sucursales})

def editarSucursal(request, id):
    sucursal = Sucursal.objects.get(id=id)
    print(sucursal)
    if request.method =='GET':
        sucursales_form = SucursalesForm(instance=sucursal)
        print(sucursales_form)
    else:
        sucursales_form = SucursalesForm(request.POST, instance=sucursal)
        if sucursales_form.is_valid():
            print(sucursales_form)
            sucursales_form.save()
        return redirect('listar_sucursales')
    return render(request, 'core/modificar_sucursal.html', {'sucursales_form': sucursales_form})

def eliminarSucursal(request,id):
    sucursal = Sucursal.objects.get(id=id)
    if request.method == 'POST':
        sucursal.save()
        sucursal.delete()
        return redirect('listar_sucursales')
    return render(request,'core/eliminar_sucursal.html', {'sucursal':sucursal})

def crearBox(request):
    sucursales = Sucursal.objects.all()
    if request.method == 'POST':
        if not request.POST._mutable:
            request.POST._mutable = True
            sucursal = Sucursal.objects.filter(id=request.POST['sucursal'])
            boxes_form = BoxesForm(request.POST)
            if boxes_form.is_valid():
                boxes_form.cleaned_data['sucursal']=sucursal
                boxes_form.save()
                return redirect('listar_boxes')
            
    else:
        boxes_form = BoxesForm()
    return render(request,'core/crear_box.html',{'boxes_form':boxes_form,'sucursales':sucursales})

def listadoBoxes(request):
    sucursal = request.user.comuna
    queryset = request.GET.get("search")
    boxes = Box.objects.filter(sucursal=sucursal)
    if queryset:
        boxes = Box.objects.filter(
            Q(estado__icontains = queryset) |Q(especialidad__icontains = queryset)
        ).distinct()

    paginator=Paginator(boxes,5)
    page=request.GET.get('page')
    boxes = paginator.get_page(page)
    return render(request,'core/listar_boxes.html',{'boxes':boxes})

def editarBox(request, id):
    box = Box.objects.get(id=id)
    if request.method =='GET':
        boxes_form = BoxesForm(instance=box)
    else:
        boxes_form = BoxesForm(request.POST, instance=box)
        if boxes_form.is_valid():
            boxes_form.save()
        return redirect('listar_boxes')
    return render(request, 'core/modificar_box.html', {'boxes_form': boxes_form})

def eliminarBox(request,id):
    box = Box.objects.get(id=id)
    if request.method == 'POST':
        box.save()
        box.delete()
        return redirect('listar_boxes')
    return render(request,'core/eliminar_box.html', {'box':box})

def crearUsuario(request):
    sucursales = Sucursal.objects.all()
    especialidades = Especialidad.objects.all()
    if request.method == 'POST':
        if not request.POST._mutable:
            request.POST._mutable = True
            # forma de acceder y modificar el diccionario para el formulario 
            request.POST['usuario_administrador'] = False
            sucursal = Sucursal.objects.filter(id=request.POST['comuna'])
            especialidad = Especialidad.objects.filter(id=request.POST['especialidad'])
            usuario_form = UsuarioForm(request.POST)
            print('este es el usuario')
            print(usuario_form.errors.as_json(),'error')
            if usuario_form.is_valid():
                print('formulario valido')
                usuario_form.cleaned_data['comuna']=sucursal
                usuario_form.cleaned_data['especialidad']=especialidad
                print(usuario_form)
                usuario_form.save()
                return redirect('login')
    else:
        usuario_form = UsuarioForm()
    return render(request,'core/crear_usuario.html',{'usuario_form':usuario_form, 'sucursales':sucursales,'especialidades':especialidades})

def crearFuncionario(request):
    sucursales = Sucursal.objects.all()
    especialidades = Especialidad.objects.all()
    if request.method == 'POST':
            if not request.POST._mutable:
                request.POST._mutable = True
                # forma de acceder y modificar el diccionario para el formulario 
                request.POST['usuario_administrador'] = True
                print(request.POST)
                sucursal = Sucursal.objects.filter(id=request.POST['comuna'])
                especialidad = Especialidad.objects.filter(id=request.POST['especialidad'])
                print(especialidad)
                usuario_form = UsuarioForm(request.POST)
                print(usuario_form)
                if usuario_form.is_valid():
                    usuario_form.cleaned_data['comuna']=sucursal
                    usuario_form.cleaned_data['especialidad']=especialidad
                    usuario_form.save()
                    return redirect('login')
    else:
        usuario_form = UsuarioForm()
    return render(request,'core/crear_funcionario.html',{'usuario_form':usuario_form, 'sucursales':sucursales,'especialidades':especialidades})

def listadoFuncionarios(request):
    id = request.user.id
    comuna = request.user.comuna
    usuarios = Usuario.objects.filter(comuna=comuna).filter(usuario_administrador=True).exclude(id=id).order_by('id')
    paginator=Paginator(usuarios,5)
    page=request.GET.get('page')
    usuarios = paginator.get_page(page)
    return render(request,'core/listar_funcionarios.html',{'usuarios':usuarios})

#filtrado de especialidad a los funcionarios
def filtrar_especialidad1(request):
    comuna = request.user.comuna
    usuarios = Usuario.objects.filter(comuna=comuna).filter(usuario_administrador=True).filter(especialidad__nombre='Enfermera').order_by('id')
    paginator=Paginator(usuarios,5)
    page=request.GET.get('page')
    usuarios = paginator.get_page(page)
    return render(request,'core/listar_funcionarios.html',{'usuarios':usuarios})

def filtrar_especialidad2(request):
    comuna = request.user.comuna
    usuarios = Usuario.objects.filter(comuna=comuna).filter(usuario_administrador=True).filter(especialidad__nombre='Kinesiología').order_by('id')
    paginator=Paginator(usuarios,5)
    page=request.GET.get('page')
    usuarios = paginator.get_page(page)
    return render(request,'core/listar_funcionarios.html',{'usuarios':usuarios})

def filtrar_especialidad3(request):
    comuna = request.user.comuna
    usuarios = Usuario.objects.filter(comuna=comuna).filter(usuario_administrador=True).filter(especialidad__nombre='Fonoaudiología').order_by('id')
    paginator=Paginator(usuarios,5)
    page=request.GET.get('page')
    usuarios = paginator.get_page(page)
    return render(request,'core/listar_funcionarios.html',{'usuarios':usuarios})

def listadoPacientes(request):
    comuna = request.user.comuna
    usuarios = Usuario.objects.filter(comuna=comuna).filter(usuario_administrador=False).order_by('id')
    paginator=Paginator(usuarios,5)
    page=request.GET.get('page')
    usuarios = paginator.get_page(page)
    return render(request,'core/listar_usuarios.html',{'usuarios':usuarios})

def filtradoPacientes1(request):
    comuna = request.user.comuna
    usuarios = Usuario.objects.filter(comuna=comuna).filter(usuario_administrador=False).filter(etapa=1).order_by('id')
    print(usuarios)
    fecha_nacimiento = usuarios
    print(fecha_nacimiento)
    paginator=Paginator(usuarios,5)
    page=request.GET.get('page')
    usuarios = paginator.get_page(page)
    return render(request,'core/listar_usuarios.html',{'usuarios':usuarios})

def filtradoPacientes2(request):
    comuna = request.user.comuna
    usuarios = Usuario.objects.filter(comuna=comuna).filter(usuario_administrador=False).filter(etapa=2).order_by('id')
    print(usuarios)
    fecha_nacimiento = usuarios
    paginator=Paginator(usuarios,5)
    page=request.GET.get('page')
    usuarios = paginator.get_page(page)
    return render(request,'core/listar_usuarios.html',{'usuarios':usuarios})

def filtradoPacientes3(request):
    comuna = request.user.comuna
    usuarios = Usuario.objects.filter(comuna=comuna).filter(usuario_administrador=False).filter(etapa=3).order_by('id')
    print(usuarios)
    fecha_nacimiento = usuarios
    paginator=Paginator(usuarios,5)
    page=request.GET.get('page')
    usuarios = paginator.get_page(page)
    return render(request,'core/listar_usuarios.html',{'usuarios':usuarios})

def editarUsuario(request,id):
    usuario = request.user.usuario_administrador
    usuario_form = None
    error = None
    try:
        usuario = Usuario.objects.get(id = id)
        print(usuario)
        password = usuario.password
        print(password)
        if request.method == 'GET':
            usuario_form = ModifyUser(instance=usuario)            
        else:
            usuario_form = ModifyUser(request.POST, instance=usuario)
            print(usuario_form.errors.as_json(),'error')
            #print(request.POST)
            if usuario_form.is_valid():
                print('debug')
                usuario_form.save()
                return redirect('listar_pacientes')
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
        return redirect('login')

    return render(request,'core/modificar_usuario.html',{'usuario_form':usuario_form})

def editar_self_funcionario(request):
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
        return redirect('login')
    return render(request,'core/modificar_funcionario.html',{'usuario_form':usuario_form})

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
    logeado = Usuario.objects.get(email=usuario)
    sucursal = logeado.comuna
    especialidad = logeado.especialidad
    if request.method == 'POST':
        if not request.POST._mutable:
            request.POST._mutable = True
            reserva_form = ReservaForm(request.POST)
            print(reserva_form.errors.as_json(),'error')
            dia_reservado = request.POST['dia_reservado']
            request.POST['usuario']=usuario
            request.POST['sucursal']=sucursal
            request.POST['especialidad']=especialidad
            reserva_form = ReservaForm(request.POST)
            if reserva_form.is_valid():
            # forma de acceder y modificar el diccionario para el formulario 
                reserva_form.cleaned_data['usuario']=usuario
                reserva_form.cleaned_data['dia_reservado']=dia_reservado
                reserva_form.save()   
                return redirect('listar_reservas_self')
    else:
        reserva_form = ReservaForm()
    return render(request,'core/crear_reserva.html',{'reserva_form':reserva_form, 'usuario':usuario,'sucursal':sucursal})


def editarReserva(request,id):
    reserva = Reserva.objects.get(id = id)
    if request.method == 'GET':
        reserva_form = ReservaForm(instance=reserva)
    else:
        reserva_form = ReservaForm(request.POST, instance=reserva)
        if reserva_form.is_valid():
            reserva_form.save()
        return redirect('listar_reservas_self')
    return render(request,'core/modificar_reserva.html',{'reserva_form':reserva_form})


def eliminarReserva(request,id):
    reserva = Reserva.objects.get(id = id)
    if request.method == 'POST':
        reserva.save()
        reserva.delete() # de esta forma se elimina fisicamente el registro
        return redirect('listar_reservas')
    return render(request, 'core/eliminar_reserva.html',{'reserva':reserva})


def crearAtencion(request,id,especialidad, sucursal):
    #se debe agregar a la fecha_hora inicial, la hora final (que debiese definirse en un rango de +1hora de atencion + 1/2 aseo+ 1/2 extra)
    fecha_hora = Reserva.objects.get(id=id)
    filter_temp = Atencion.objects.filter(reserva__dia_reservado=fecha_hora.dia_reservado)
    lista_ocupados = filter_temp.values_list('especialista__id')
    print(lista_ocupados)
    lista_box = filter_temp.values_list('box__id')

    print(fecha_hora.dia_reservado)
    especialidad = Especialidad.objects.filter(nombre=especialidad)
    print(especialidad)
    sucursal = Sucursal.objects.get(nombre=sucursal)
    especialistas = Usuario.objects.filter(Q(especialidad__in = especialidad)& Q(usuario_administrador = True)).exclude(id__in=lista_ocupados)
    print(especialistas)
    print(sucursal)
    reservas = Reserva.objects.filter(id=id)
    boxes = Box.objects.filter(Q(especialidad__in=especialidad)&Q(estado__in='1')&Q(sucursal__nombre=sucursal)).exclude(id__in=lista_box)
    if request.method == 'POST':
        if not request.POST._mutable:
            request.POST._mutable = True
            especialista = Especialidad.objects.filter(id=request.POST['especialista'])
            atencion_form = AtencionForm(request.POST)
            if atencion_form.is_valid():
                atencion_form.cleaned_data['especialista']=especialista
                atencion_form.save()
                return redirect('listar_atenciones')
    else:
        atencion_form = AtencionForm()
    return render(request,'core/crear_atencion.html',{'atencion_form':atencion_form,'especialistas':especialistas, 'reservas':reservas,'boxes':boxes})

def editarAtencion(request,id):
    atencion = Atencion.objects.get(id = id)
    if request.method == 'GET':
        atencion_form = AtencionForm(instance=atencion)
    else:
        atencion_form = AtencionForm(request.POST, instance=atencion)
        if atencion_form.is_valid():
            atencion_form.save()
        return redirect('listar_atenciones')
    return render(request,'core/modificar_atencion.html',{'atencion_form':atencion_form})

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
    today = date.today()
    id = request.user.id
    queryset = request.GET.get("search")
    print(id)
    reservas = Reserva.objects.filter(usuario=id).order_by('id')
    paginator=Paginator(reservas,5)
    page=request.GET.get('page')
    reservas = paginator.get_page(page)
    return render(request,'core/listar_mis_reservas.html',{'reservas':reservas})

def listadoReservas(request):
    comuna = request.user.comuna
    reservas = Reserva.objects.filter(usuario__comuna=comuna).order_by('id')
    paginator=Paginator(reservas,5)
    page=request.GET.get('page')
    reservas = paginator.get_page(page)
    return render(request,'core/listar_reservas.html',{'reservas':reservas})

def listadoReservasToday(request):
    today = date.today()
    comuna = request.user.comuna
    reservas = Reserva.objects.filter(usuario__comuna=comuna).filter(dia_reservado__year=today.year, dia_reservado__month=today.month, dia_reservado__day=today.day).order_by('id')
    paginator=Paginator(reservas,5)
    page=request.GET.get('page')
    reservas = paginator.get_page(page)
    return render(request,'core/listar_reservas.html',{'reservas':reservas})

def listadoReservasKine(request):
    today = date.today()
    comuna = request.user.comuna
    reservas = Reserva.objects.filter(usuario__comuna=comuna).filter(especialidad='Kinesiología').order_by('id')
    paginator=Paginator(reservas,5)
    page=request.GET.get('page')
    reservas = paginator.get_page(page)
    return render(request,'core/listar_reservas.html',{'reservas':reservas})

def listadoReservasFono(request):
    today = date.today()
    comuna = request.user.comuna
    reservas = Reserva.objects.filter(usuario__comuna=comuna).filter(especialidad='Fonoaudiología').order_by('id')
    paginator=Paginator(reservas,5)
    page=request.GET.get('page')
    reservas = paginator.get_page(page)
    return render(request,'core/listar_reservas.html',{'reservas':reservas})


def listadoAtenciones(request):
    atenciones = Atencion.objects.all()
    paginator=Paginator(atenciones,5)
    page=request.GET.get('page')
    atenciones = paginator.get_page(page)
    return render(request,'core/listar_atenciones.html',{'atenciones':atenciones})

def listadoAtencionesToday(request):
    today = date.today()
    atenciones = Atencion.objects.filter(reserva__dia_reservado__year=today.year, reserva__dia_reservado__month=today.month, reserva__dia_reservado__day=today.day).order_by('id')
    paginator=Paginator(atenciones,5)
    page=request.GET.get('page')
    atenciones = paginator.get_page(page)
    return render(request,'core/listar_atenciones.html',{'atenciones':atenciones})


def listadoAtencionesSelf(request):
    id = request.user.id
    atenciones = Atencion.objects.filter(especialista=id).order_by('id')
    paginator=Paginator(atenciones,5)
    page=request.GET.get('page')
    atenciones = paginator.get_page(page)
    return render(request,'core/listar_mis_atenciones.html',{'atenciones':atenciones})

def listadoAtencionesSelfToday(request):
    today = date.today()
    id = request.user.id
    atenciones = Atencion.objects.filter(especialista=id).filter(reserva__dia_reservado__year=today.year, reserva__dia_reservado__month=today.month, reserva__dia_reservado__day=today.day).order_by('id')
    paginator=Paginator(atenciones,5)
    page=request.GET.get('page')
    atenciones = paginator.get_page(page)
    return render(request,'core/listar_mis_atenciones.html',{'atenciones':atenciones})

class actualizarAtencion(UpdateView):
    model = Atencion
    template_name = 'core/crear_atencion.html'
    form_class = AtencionForm
    success_url = reverse_lazy('core:listar_atenciones')

def iniciarAtencion(request,id):
    atencion = Atencion.objects.get(id = id)
    usuario = atencion.reserva.usuario
    print(usuario)
    insumos = allInsumos().get('consultas')
    print(insumos)
    return render(request, 'core/iniciar_atencion.html', {'usuario':usuario,'insumos':insumos})

def allInsumos():
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT ID_INSUMO,NOMBRE_INSUMO,ESPECIALIDAD,STOCK FROM INSUMO")
        rawData = cursor.fetchall()
        result = []
        for r in rawData:
            result.append(list(r))
        contexto = {'consultas': result }
    return contexto

def insumo(request):
    return render(request, 'core/insumo.html', allInsumos())


# #revisar como hacer triggers y updates
# def actualizarStock(request, id, cant):
#     from django.db import connection
#     with connection.cursor() as cursor:
#         #cursor.execute("UPDATE ID_INSUMO,NOMBRE_INSUMO,ESPECIALIDAD,STOCK FROM INSUMO") vista original
#         cursor.execute("UPDATE")