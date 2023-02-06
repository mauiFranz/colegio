from django.contrib import admin

from core.cursos.models import Nivel, Grado, Curso, Educacion


class EstablecimientoModelAdmin(admin.ModelAdmin):
    list_display = ['nombre_establecimiento', 'tipo_establecimiento', 'comuna_establecimiento']


class EducacionModelAdmin(admin.ModelAdmin):
    list_display = ['codigo_educacion', 'nombre_educacion', 'vigente_educacion', 'fecha_creacion_educacion', 'fecha_ini_vig_educacion', 'fecha_fin_vig_educacion']


class NivelModelAdmin(admin.ModelAdmin):
    list_display = ['codigo_nivel', 'nombre_nivel', 'educacion_nivel', 'vigente_nivel', 'fecha_creacion_nivel', 'fecha_ini_vig_nivel', 'fecha_fin_vig_nivel']


class GradoModelAdmin(admin.ModelAdmin):
    list_display = ['codigo_grado', 'nombre_grado', 'nivel_grado', 'vigente_grado', 'fecha_creacion_grado', 'fecha_ini_vig_grado', 'fecha_fin_vig_grado']


class CursoModelAdmin(admin.ModelAdmin):
    list_display = ['codigo_curso', 'paralelo_curso', 'anno_curso', 'grado_curso', 'vigente_curso', 'fecha_creacion_curso', 'fecha_ini_vig_curso', 'fecha_fin_vig_curso']



admin.site.register(Educacion, EducacionModelAdmin)
admin.site.register(Nivel, NivelModelAdmin)
admin.site.register(Grado, GradoModelAdmin)
admin.site.register(Curso, CursoModelAdmin)