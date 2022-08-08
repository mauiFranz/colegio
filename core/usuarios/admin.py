from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.usuarios import models
from core.usuarios import forms



# Register your models here.
class CustomUserAdmin(UserAdmin):
    form = forms.CustomUserChangeForm
    add_form = forms.CustomUserCreationForm
    fieldsets = (
        (
            'Datos Seguridad', {
                'fields': (
                    'username',
                    'run_user',
                    'dv_user',
                    'password',
                    'email',
                )
            }
        ),
        (
            'Datos Personales', {
                'fields': (
                    'first_name',
                    'snombre_user',
                    'last_name',
                    'apmat_user',
                    'foto_user',
                    'fecha_nac_user',
                )
            }
        ),
        (
            'Datos Contacto', {
                'fields': (
                    'celular_user',
                    'direccion_user',
                    'comuna_user',
                )
            }
        ),
        (
            'Permisos', {
                'fields': (
                    'is_admin',
                    'is_alumno',
                    'is_profesor',
                    'is_administrativo',
                    'is_apoderado',
                    'is_inspector',
                    'is_auditor',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            }
        ),
        (
            'Fechas', {
                'fields': (
                    'last_login',
                    'date_joined',
                )
            }
        )
    )
    list_display = ['username', 'run_user', 'dv_user', 'first_name', 'last_name', 'apmat_user', 'email']


class RegionModelAdmin(admin.ModelAdmin):
    list_display = ['codigo_region', 'nombre_region', 'orden_region']


class ProvinciaModelAdmin(admin.ModelAdmin):
    list_display = ['codigo_provincia', 'nombre_provincia', 'region_provincia']
    

class ComunaModelAdmin(admin.ModelAdmin):
    list_display = ['codigo_comuna', 'nombre_comuna', 'provincia_comuna']
    
    
admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.UserAdmin)
admin.site.register(models.UserAdministrativo)
admin.site.register(models.UserAlumno)
admin.site.register(models.UserApoderado)
admin.site.register(models.UserAuditor)
admin.site.register(models.UserInspector)
admin.site.register(models.UserProfesor)
admin.site.register(models.Region, RegionModelAdmin)
admin.site.register(models.Provincia, ProvinciaModelAdmin)
admin.site.register(models.Comuna, ComunaModelAdmin)
