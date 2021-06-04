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

    def __str__(self):
        return f'Usuario {self.email}'

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

    def _str_(self):
        return f'Reserva {self.dia_reservado}'
    

class Atencion(models.Model):
    id = models.AutoField(primary_key= True)
    reserva = models.OneToOneField(Reserva, on_delete=CASCADE)
    nombre_especialista = models.CharField(max_length=20)
    apellido_especialista = models.CharField(max_length=20)
    box = models.CharField(max_length=10)
    
    class Meta:
        verbose_name = 'Atencion'
        verbose_name_plural = 'Atenciones'
        ordering = ['reserva_id']

    def _str_(self):
        return "{0},{1}".format(self.reserva_id, self.reserva_id)
