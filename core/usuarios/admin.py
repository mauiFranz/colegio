from django.contrib import admin

from core.usuarios import models


# Register your models here.
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['username', 'run_user', 'dv_user', 'first_name', 'last_name', 'apmat_user', 'email']
    

class RegionModelAdmin(admin.ModelAdmin):
    list_display = ['codigo_region', 'nombre_region', 'orden_region']


    
admin.site.register(models.User, UserModelAdmin)
admin.site.register(models.UserAdmin)
admin.site.register(models.UserAdministrativo)
admin.site.register(models.UserAlumno)
admin.site.register(models.UserApoderado)
admin.site.register(models.UserAuditor)
admin.site.register(models.UserInspector)
admin.site.register(models.UserProfesor)
admin.site.register(models.Region, RegionModelAdmin)
admin.site.register(models.Provincia)
admin.site.register(models.Comuna)
