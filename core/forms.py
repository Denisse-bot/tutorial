from django import forms
from django.contrib.auth.password_validation import password_changed
from django.db import models
from django.db.models import fields
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import widgets
from .models import Atencion, Especialidad, Reserva, Sucursal, Usuario, Box


class FormularioLogin(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super(FormularioLogin, self).__init__(self,*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contrasena'

class SucursalesForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = [
            'nombre',
            'direccion'
        ]
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre de la sucursal'
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la direccion del centro de atención del especialista'
                }
            ),
        }

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
        'comuna',
        'especialidad',
        'usuario_administrador'
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
            'fecha_nacimiento':forms.DateInput(format='%d/%m/%Y'
            ,attrs={
                'class': 'form-class',
                'placeholder': '01/12/1990'
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
            'usuario_administrador': forms.HiddenInput(
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

class ModifyUserSelf(forms.ModelForm):
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
        'comuna',
        'especialidad',
        'etapa',
        'usuario_administrador'
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
            'fecha_nacimiento':forms.DateInput(format='%d/%m/%Y'
            ,attrs={
                'class': 'form-class',
                'placeholder': '01/12/1990'
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
            'etapa': forms.HiddenInput(
            ),
            'usuario_administrador': forms.HiddenInput(
            ),
        }
    def save(self,commit = True):
        user = super().save(commit = False)
        if commit:
            user.save()
        return user

class ModifyUser(forms.ModelForm):
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
        'comuna',
        'especialidad',
        'etapa',
        'usuario_administrador'
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
            'fecha_nacimiento':forms.DateInput(format='%d/%m/%Y'
            ,attrs={
                'class': 'form-class',
                'placeholder': '01/12/1990'
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
            'etapa': forms.Select(
                attrs={
                    'class': 'form-control'                    
                }
            ),
            'usuario_administrador': forms.HiddenInput(
            ),
        }
    def save(self,commit = True):
        user = super().save(commit = False)
        if commit:
            user.save()
        return user

class ModifyFuncionario(forms.ModelForm):
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
        'comuna',
        'especialidad',
        'etapa',
        'usuario_administrador'
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
            'fecha_nacimiento':forms.DateInput(format='%d/%m/%Y'
            ,attrs={
                'class': 'form-class',
                'placeholder': '01/12/1990'
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
            'etapa': forms.HiddenInput(
            ),
            'usuario_administrador': forms.HiddenInput(
            ),
        }
    def save(self,commit = True):
        user = super().save(commit = False)
        if commit:
            user.save()
        return user

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields =[
            'nombre'
        ]
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-class',
                    'placeholder': 'Ingrese el nombre de la especialidad'
                }
            )
        }


class ReservaForm(forms.ModelForm):
    
    class Meta: 
        model = Reserva
        fields = [
            'dia_reservado',
            'usuario',
            'sucursal',
            'especialidad'
        ]
        widgets = {
            'dia_reservado':forms.DateTimeInput(format='%d/%m/%Y %H:%M'
            ,attrs={
                'class': 'form-class',
                'placeholder': '01/12/1990'
                }
            ),

            'usuario': forms.HiddenInput(
            ),
            'sucursal': forms.HiddenInput(
            ),
            'especialidad': forms.HiddenInput(
            )
        }

class BoxesForm(forms.ModelForm):
    
    class Meta: 
        model = Box
        fields = [
            'estado',
            'especialidad',
            'tamaño',
            'sucursal',
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
            ),
            'tamaño': forms.Select(
                attrs={
                    'class': 'form-control'                    
                }
            ),
            'sucursal': forms.Select(
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
            'especialista',
            'box'
         ]
        widgets = {
            'reserva': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'especialista': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Seleccione el nombre del especialista',
                }
            ),
            'box': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            )
        }

class iniciarAtencionForm(forms.ModelForm):
    class Meta:
        model = Atencion
        fields = [
            'extendida',
            'comentarios'
        ]
        widgets = {
            'extendida': forms.RadioSelect(),
            'comentarios': forms.Textarea(
            )
        }

# class iniciarAtencionForm(forms.ModelForm):
    
#     class Meta: 
#         model = Atencion
#         fields = [
#             'extendida',
#             'comentarios'
#         ]
#         widgets = {
#             'extendida': forms.BooleanField(),
#             'comentarios': forms.Textarea(
#             )
#         }