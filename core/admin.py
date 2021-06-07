
from django.contrib import admin
from django.contrib.admin import models
from .models import Atencion, Usuario, Reserva
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class UsuarioResource(resources.ModelResource):
    class Meta:
        model = Usuario

class UsuarioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['rut','email']
    list_display = ['id','nombre','apellido','rut','email','usuario_administrador']
    resources_class = UsuarioResource

class ReservaResource(resources.ModelResource):
    class Meta:
        model = Reserva

class ReservaAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['especialidad','dia_reservado','sucursal','usuario_id']
    list_display = ['especialidad','dia_reservado','sucursal','usuario_id']
    resource_class = ReservaResource

class AtencionResource(resources.ModelResource):
    class Meta:
        model = Atencion

class AtencionAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['id','reserva_id','box']
    list_display = ['id','reserva_id','nombre_especialista','apellido_especialista','box']
    resource_class = AtencionResource

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Reserva,ReservaAdmin)
admin.site.register(Atencion, AtencionAdmin)