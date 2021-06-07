from typing import OrderedDict
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import AutoField, EmailField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class UsuarioManager(BaseUserManager):
    def create_user(self,username,email,nombre,apellido,rut,fecha_nacimiento,direccion,nro_direccion,comuna=None, password=None):
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
            comuna = comuna
        )
        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self,username,email,nombre,apellido,rut,fecha_nacimiento,direccion,nro_direccion,comuna,password):
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
            password = password
        )
        usuario.usuario_administrador = True
        usuario.save()
        return usuario

class Usuario(AbstractBaseUser):
    comuna_list = (
        (1, 'Providencia'), 
        (2, 'San Bernardo'),
        (3, 'La Serena'),
        (4, 'Temuco')
    )
    username=models.CharField('Nombre de usuario', max_length=100, unique=True)
    email=models.EmailField('Correo Electronico',max_length=50, unique=True, blank=True, null=True)
    nombre=models.CharField('Nombre',max_length=50)
    apellido=models.CharField('Apellido',max_length=50)
    rut=models.CharField('Rut',max_length=15, unique=True, blank=True, null=True)
    fecha_nacimiento=models.DateField('Fecha Nacimiento', blank=True, null=True)
    direccion=models.CharField('Dirección',max_length=50, blank=True, null=True)
    nro_direccion=models.IntegerField('Nro Direccion', blank=True, null=True)
    comuna=models.IntegerField(choices=comuna_list, default=1, blank=True, null=True)
    usuario_activo = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    fecha_creacion = models.DateField('Fecha de creación', auto_now=True,auto_now_add=False)
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','nombre','apellido','rut','fecha_nacimiento','direccion','nro_direccion','comuna']

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

class Reserva(models.Model):
    id = models.AutoField(primary_key= True)
    tipo_terapia = (
    (1, 'Kinesiología'),
    (2, 'Fonoaudiología'),
    (3, 'General')
    )
    sucursal_list = (
        (1, 'Providencia'),
        (2, 'San Bernardo'),
        (3, 'La Serena'),
        (4, 'Temuco')
    )

    especialidad=models.IntegerField(choices=tipo_terapia, default=3)
    dia_reservado=models.DateTimeField()
    sucursal=models.IntegerField(choices=sucursal_list, default=1, blank=True, null=True)
    usuario=models.ForeignKey('core.Usuario', on_delete=CASCADE)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['sucursal']

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
    especialidad_list=(
        (1, 'Fonoaudiologia'),
        (2, 'Kinesiologia'),
        (3, 'General')
    )

    id = models.AutoField(primary_key= True)
    estado = models.IntegerField(choices=estado_list, default=None)
    especialidad = models.IntegerField(choices=especialidad_list, default=None)
    
    class Meta:
        verbose_name = 'Box'
        verbose_name_plural = 'Boxes'
        ordering = ['estado']

    def __str__(self):
        id=self.id
        especialidad=self.especialidad
        if especialidad==1:
            especialidad='Fonoaudiologia'
        else:
            especialidad='Kinesiologia'
        box=str(id)+","+str(especialidad)
        return box


class Atencion(models.Model):
    id = models.AutoField(primary_key= True)
    reserva = models.OneToOneField(Reserva, on_delete=CASCADE)
    nombre_especialista = models.CharField(max_length=20)
    apellido_especialista = models.CharField(max_length=20)
    box = models.ForeignKey(Box, on_delete=CASCADE)
    
    class Meta:
        verbose_name = 'Atencion'
        verbose_name_plural = 'Atenciones'
        ordering = ['reserva_id']

    def __str__(self):
        atencion=self.reserva+","+self.box
        return atencion
