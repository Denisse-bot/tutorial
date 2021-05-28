from django import forms
from django.db import models
from django.db.models import fields
from .models import Atencion, Reserva, Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
        'nombre',
        'apellido',
        'rut',
        'fecha_nacimiento',
        'email',
        'direccion',
        'nro_direccion',
        'comuna'
        ]

class ReservaForm(forms.ModelForm):
    
    class Meta: 
        model = Reserva
        fields = [
            'especialidad',
            'dia_reservado',
            'sucursal',
            'usuario'
        ]

class AtencionForm(forms.ModelForm):
    class Meta:
        model = Atencion
        fields = [
            'reserva',
            'nombre_especialista',
            'apellido_especialista',
            'box'
         ]