from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from core.usuarios.models import Comuna


class Establecimiento(models.Model):
    TIPOS = {
		(1, 'Urbano'),
		(2, 'Rural'),
	}
    nombre_establecimiento = models.CharField(max_length=150)
    fecha_inauguracion_establecimiento = models.DateField(null=True, blank=True)
    sostenedor_establecimiento = models.CharField(max_length=75, null=True, blank=True)
    tipo_establecimiento = models.CharField(max_length=15, choices=TIPOS)
    proyecto_educativo = models.FileField(null=True, blank=True)
    direccion_establecimiento = models.CharField(max_length=250)
    comuna_establecimiento = models.ForeignKey(Comuna, on_delete=models.PROTECT)
    is_active_establecimiento = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre_establecimiento
    
    class Meta:
        verbose_name = 'Establecimiento'
        verbose_name_plural = 'Establecimientos'
        ordering = ['comuna_establecimiento', 'nombre_establecimiento']
    
    
class Educacion(models.Model):
    """ Este modelo almacena los tipos de educación
        Parvularia, Básica, Media y Superior
    """
    codigo_educacion = models.PositiveIntegerField(primary_key=True)
    nombre_educacion = models.CharField(max_length=35)
    vigente_educacion = models.BooleanField(default=True)
    fecha_creacion_educacion = models.DateTimeField(auto_now_add=True)
    fecha_ini_vig_educacion = models.DateTimeField()
    fecha_fin_vig_educacion = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre_educacion

    class Meta:
        verbose_name = 'Educación'
        verbose_name_plural = 'Educaciones'
        ordering = ['codigo_educacion', 'vigente_educacion']


class Nivel(models.Model):
    """ Este modelo almacena los niveles en la educación 
        chilena: sala cuna, medio, transición, ciclo I, ciclo II,
        emch, emtp (ch), emtp (esp), cft, ip, universidad.

    """
    codigo_nivel = models.PositiveIntegerField(primary_key=True)
    nombre_nivel = models.CharField(max_length=20)
    vigente_nivel = models.BooleanField(default=True)
    fecha_creacion_nivel = models.DateTimeField(auto_now_add=True)
    fecha_ini_vig_nivel = models.DateTimeField()
    fecha_fin_vig_nivel = models.DateTimeField(null=True, blank=True)
    educacion_nivel = models.ForeignKey(Educacion, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.nombre_nivel
    
    class Meta:
        verbose_name = 'Nivel'
        verbose_name_plural = 'Niveles'
        ordering = ['educacion_nivel', 'codigo_nivel', 'vigente_nivel']


class Grado(models.Model):
    """ Este modelo es el equivalente a los grados en 
        la educación chilena: primero, segundo, tercero,
        cuarto ... octavo.

    """
    codigo_grado = models.PositiveIntegerField(primary_key=True)
    nombre_grado = models.CharField(max_length=15)
    fecha_creacion_grado = models.DateField(auto_now_add=True)
    fecha_ini_vig_grado = models.DateTimeField()
    fecha_fin_vig_grado = models.DateTimeField(null=True, blank=True)
    vigente_grado = models.BooleanField(default=True)
    nivel_grado = models.ForeignKey(Nivel, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.nombre_grado
    
    class Meta:
        verbose_name = 'Grado'
        verbose_name_plural = 'Grados'
        ordering = ['nivel_grado', 'codigo_grado', 'vigente_grado']



class Curso(models.Model):
    """ Este módelo almacena los cursos o paralelos de 
        cada grado: "A", "B", "C" ...
    """
    codigo_curso = models.PositiveIntegerField(primary_key=True)
    paralelo_curso = models.CharField(max_length=2)
    anno_curso = models.PositiveIntegerField(validators=[MaxValueValidator(9999), MinValueValidator(1980)])
    vigente_curso = models.BooleanField(default=True)
    fecha_creacion_curso = models.DateTimeField(auto_now_add=True)
    fecha_ini_vig_curso = models.DateTimeField()
    fecha_fin_vig_curso = models.DateTimeField(null=True, blank=True)
    grado_curso = models.ForeignKey(Grado, on_delete=models.PROTECT)
    
    
    def __str__(self):
        return self.paralelo_curso

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['grado_curso', 'codigo_curso', 'vigente_curso']

