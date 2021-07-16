from typing import OrderedDict
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import AutoField, EmailField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class Especialidad(models.Model):
    id = models.AutoField(primary_key= True)
    nombre = models.CharField('Especialidad',max_length=40, unique=True, null=True)
    

    class Meta:
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidad'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Sucursal(models.Model):
    id = models.AutoField(primary_key= True)
    nombre = models.CharField('Sucursal',max_length=40, unique=True, null=True)
    direccion = models.CharField('Dirección', max_length=60,blank=True)

    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class UsuarioManager(BaseUserManager):
    def create_user(self,username,email,nombre,apellido,rut,fecha_nacimiento,direccion,nro_direccion,usuario_administrador,comuna,especialidad,etapa,password=None):
        if not email:
            raise ValueError('El usuario debe ingresar un correo electrónico')

        usuario = self.model(
            username = username,
            email = self.normalize_email(email),
            nombre = nombre,
            apellido = apellido,
            rut = rut,
            fecha_nacimiento = fecha_nacimiento,
            direccion = direccion,
            nro_direccion = nro_direccion,
            comuna = comuna,
            especialidad = especialidad,
            etapa = etapa,
            usuario_administrador = usuario_administrador,
        )
        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self,username,email,nombre,apellido,rut,fecha_nacimiento,direccion,nro_direccion,comuna,especialidad,etapa,password):
        usuario = self.create_user(
            username = username,
            email = email,
            nombre = nombre,
            apellido = apellido,
            rut = rut,
            fecha_nacimiento = fecha_nacimiento,
            direccion = direccion,
            nro_direccion = nro_direccion,
            comuna = comuna,
            especialidad=especialidad,
            etapa = etapa,
            password = password,
            usuario_administrador = True
        )
        usuario.save()
        return usuario

class Usuario(AbstractBaseUser):

    etapa_list=(
        (0, 'Sin etapa'),
        (1, 'Primera'),
        (2, 'Segunda'),
        (3, 'Tercera')
    )
    username=models.CharField('Nombre de usuario', max_length=100, unique=True)
    email=models.EmailField('Correo Electronico',max_length=50, unique=True, blank=True, null=True)
    nombre=models.CharField('Nombre',max_length=50)
    apellido=models.CharField('Apellido',max_length=50)
    rut=models.CharField('Rut',max_length=15, unique=True, blank=True, null=True)
    fecha_nacimiento=models.DateField('Fecha Nacimiento', blank=True, null=True)
    direccion=models.CharField('Dirección',max_length=50, blank=True, null=True)
    nro_direccion=models.IntegerField('Nro Direccion', blank=True, null=True)
    comuna=models.ForeignKey(Sucursal, on_delete=CASCADE)
    especialidad=models.ForeignKey(Especialidad,on_delete=CASCADE)
    usuario_activo = models.BooleanField(default=True)
    etapa = models.IntegerField('Etapa',choices=etapa_list,default=0,null=True, blank=True)
    usuario_administrador = models.BooleanField(default=False)
    fecha_creacion = models.DateField('Fecha de creación', auto_now=True,auto_now_add=False)
    objects = UsuarioManager()


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','nombre','apellido','rut','fecha_nacimiento','direccion','nro_direccion','comuna','especialidad','usuario_administrador']
    

    #revisar luego si quiero llamarlo usuario o paciente
    def __str__(self):
        return self.email

    def has_perm(self,perm,obj = None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_administrador
    @property
    def is_nurse(self):
        especialidad = False
        if self.especialidad.nombre == 'Enfermera':
            especialidad = True
        return especialidad

# class Funcionario(Usuario):
#     tipo_especialidad = (
#     (1, 'Kinesiología'),
#     (2, 'Fonoaudiología'),
#     (3, 'Enfermero/Funcionario')
#     )
#     especialidad = models.IntegerField(choices=tipo_especialidad, default=1, blank=True, null=True)

# class Paciente(Usuario):
#     patologia = models.TextField(max_length=500)



class Reserva(models.Model):
    id = models.AutoField(primary_key= True)
    dia_reservado=models.DateTimeField()
    usuario=models.ForeignKey('core.Usuario', on_delete=CASCADE)
    sucursal = models.CharField('sucursal', max_length=50)
    especialidad = models.CharField('especialidad', max_length=20)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['dia_reservado']

    def __str__(self):
        dia_reservado=self.dia_reservado
        usuario=self.usuario
        reserva=str(dia_reservado)+","+str(usuario)
        return reserva


class Box(models.Model):
    estado_list=(
        (1, 'Disponible'),
        (2, 'En atención'),
        (3, 'En mantención'),
        (4, 'No disponible, deshabilitada')
    )
    tamaño_list=(
        (1, 'Grande'),
        (2, 'Mediano'),
        (3, 'Pequeño')
    )

    id = models.AutoField(primary_key= True)
    estado = models.IntegerField(choices=estado_list, default=None)
    tamaño = models.IntegerField(choices=tamaño_list,default=None)
    especialidad = models.ForeignKey(Especialidad, on_delete=CASCADE)
    sucursal=models.ForeignKey(Sucursal, on_delete=CASCADE)
    class Meta:
        verbose_name = 'Box'
        verbose_name_plural = 'Boxes'
        ordering = ['estado']

    def __str__(self):
        id = str(self.id)
        especialidad=str(self.especialidad)
        #tamaño=str(self.tamaño)
        return  id +' '+ especialidad


class Atencion(models.Model):
    id = models.AutoField(primary_key= True)
    reserva = models.OneToOneField(Reserva, on_delete=CASCADE)
    especialista = models.ForeignKey(Usuario, on_delete=CASCADE)
    box = models.ForeignKey(Box, on_delete=CASCADE)
    extendida = models.BooleanField(default=False)
    comentarios = models.TextField(max_length=300)
    
    class Meta:
        verbose_name = 'Atencion'
        verbose_name_plural = 'Atenciones'
        ordering = ['reserva_id']

    def __str__(self):
        atencion=str(self.id)
        return atencion
