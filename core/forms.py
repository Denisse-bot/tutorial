from django import forms
from django.contrib.auth.password_validation import password_changed
from django.db import models
from django.db.models import fields
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import widgets
from .models import Atencion, Reserva, Usuario, Box
from datetimewidget.widgets import DateTimeWidget


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
                    'placeholder':'Ingrese su Rut: 12.345.678-9',
                }            
            ),
            'fecha_nacimiento':DateTimeWidget(
                attrs={
                    'id':"yourdatetimeid"
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
            'comuna': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Contraseñas no coinciden')
        return password2
    
    def save(self,commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user



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
            'especialidad': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'dia_reservado': forms.SelectDateWidget(),
            'sucursal': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'usuario': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            )
        }

class BoxesForm(forms.ModelForm):
    
    class Meta: 
        model = Box
        fields = [
            'estado',
            'especialidad'
        ]
        widgets = {
            'estado': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'especialidad': forms.Select(
                attrs={
                    'class': 'form-control'                    
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
        widgets = {
            'reserva': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'nombre_especialista': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Ingrese el nombre del especialista',
                }
            ),
            'apellido_especialista': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el apellido del especialista'
                }
            ),
            'box': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            )
        }