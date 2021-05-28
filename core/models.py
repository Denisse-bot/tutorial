from typing import OrderedDict
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import AutoField

# Create your models here.

class Usuario(models.Model):
    comuna_list = (
        (1, 'Providencia'),
        (2, 'San Bernardo'),
        (3, 'La Serena'),
        (4, 'Temuco')
    )
    id = models.AutoField(primary_key= True)
    nombre=models.CharField(max_length=50)
    apellido=models.CharField(max_length=50)
    rut=models.CharField(max_length=15, unique=True, blank=True, null=True)
    fecha_nacimiento=models.DateField( blank=True, null=True)
    email=models.EmailField(max_length=50, unique=True, blank=True, null=True)
    direccion=models.CharField(max_length=50, blank=True, null=True)
    nro_direccion=models.IntegerField( blank=True, null=True)
    comuna=models.IntegerField(choices=comuna_list, default=1, blank=True, null=True)
    usuario_activo = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    fecha_creacion = models.DateField('Fecha de creación', auto_now=True,auto_now_add=False)


    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['comuna']


    def _str_(self):
        return self.nombre

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
        return self.dia_reservado

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
