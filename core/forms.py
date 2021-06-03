from django import forms
from django.contrib.auth.password_validation import password_changed
from django.db import models
from django.db.models import fields
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import widgets
from .models import Atencion, Reserva, Usuario

class FormularioLogin(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super(FormularioLogin, self).__init__(self,*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contrasena'

class UsuarioForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña',widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'ingrese su contraseña',
            'id':'password1',
            'required':'required',
        }
    ))
    password2 = forms.CharField(label='Contraseña de confirmación',widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'ingrese su contraseña',
            'id':'password2',
            'required':'required',
        }
    ))

    class Meta:
        model = Usuario
        fields = [
        'username',
        'nombre',
        'apellido',
        'rut',
        'fecha_nacimiento',
        'email',
        'direccion',
        'nro_direccion',
        'comuna'
        ]
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Ingrese su nombre de usuario',
                }
            ),
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Ingrese su nombre',
                }
            ),
            'apellido': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Ingrese su apellido',
                }
            ),
            'rut': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Ingrese su Rut',
                }
            ),
            'fecha_nacimiento': forms.DateInput(
                attrs={
                    'class': 'datepicker',
                    'placeholder':'Ingrese su fecha de nacimiento',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Ingrese su email',
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Ingrese su dirección',
                }
            ),
            'nro_direccion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Ingrese su nro de direccion',
                }
            ),
            'comuna': forms.NumberInput(
                
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Ingrese su nombre de usuario',
                }
            ),
        }

class ReservaForm(forms.ModelForm):
    
    class Meta: 
        model = Reserva
        fields = [
            'especialidad',
            'dia_reservado',
            'sucursal',
            'usuario'
        ]
        widgets = {
            'especialidad': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Ingrese su especialidad',
                }
            ),
            'dia_reservado': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Ingrese su día a reservar',
                }
            ),
            'sucursal': forms.NumberInput(

            ),
            'usuario.nombre, usuario.apellido': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Ingrese su usuario',
                }
            )
        }

class AtencionForm(forms.ModelForm):
    class Meta:
        model = Atencion
        fields = [
            'reserva',
            'nombre_especialista',
            'apellido_especialista',
            'box'
         ]