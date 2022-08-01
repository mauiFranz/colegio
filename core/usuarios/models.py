from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator


# Create your models here.
class Region(models.Model):
    codigo_region = models.PositiveIntegerField(primary_key=True)
    nombre_region = models.CharField(max_length=75)
    orden_region = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre_region

    class Meta:
        ordering = ['orden_region']
        verbose_name = 'Región'
        verbose_name_plural = 'Regiones'


class Provincia(models.Model):
    codigo_provincia = models.PositiveIntegerField(primary_key=True)
    nombre_provincia = models.CharField(max_length=50)
    region_provincia = models.ForeignKey(Region, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre_provincia

    class Meta:
        ordering = ['nombre_provincia']
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'


class Comuna(models.Model):
    codigo_comuna = models.PositiveIntegerField(primary_key=True)
    nombre_comuna = models.CharField(max_length=50)
    provincia_comuna = models.ForeignKey(Provincia, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre_comuna

    class Meta:
        ordering = ['nombre_comuna']
        verbose_name = 'Comuna'
        verbose_name_plural = 'Comunas'


class User(AbstractUser):
    """ Clase abstracta que unifica la funcionalidad y atributos de todos los usuarios
        reemplaza al usuario básico de django
    """
    dv_user = models.CharField(max_length=1)
    snombre_user = models.CharField(max_length=25, null=True, blank=True)
    apmat_user = models.CharField(max_length=25)
    celular_user = models.IntegerField(unique=True)
    direccion_user = models.CharField(max_length=100)
    comuna_user = models.ForeignKey(Comuna, on_delete=models.PROTECT)
    foto = models.ImageField(upload_to='uploads/fotos/', null=True, blank=True, validators=[FileExtensionValidator(['png'])])
    fecha_nac_user = models.DateField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_alumno = models.BooleanField(default=False)
    is_profesor = models.BooleanField(default=False)
    is_administrativo = models.BooleanField(default=False)
    is_apoderado = models.BooleanField(default=False)
    is_inspector = models.BooleanField(default=False)
    is_auditor = models.BooleanField(default=False)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    class Meta:
        db_table = 'auth_user'
        ordering = ['username']
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        
    def get_admin_perfil(self):
        admin_perfil = None
        if hasattr(self, 'useradmin'):
            admin_perfil = self.get_useradmin
        return admin_perfil
    
    def get_alumno_perfil(self):
        alumno_perfil = None
        if hasattr(self, 'useralumno'):
            alumno_perfil = self.get_useralumno
        return alumno_perfil
    
    def get_prof_perfil(self):
        prof_perfil = None
        if hasattr(self, 'userprof'):
            prof_perfil = self.get_userprof
        return prof_perfil
            
    def get_administrativo_perfil(self):
        administrativo_perfil = None
        if hasattr(self, 'useradministrativo'):
            administrativo_perfil = self.get_useradministrativo
        return administrativo_perfil
    
    def get_apoderado_perfil(self):
        apoderado_perfil = None
        if hasattr(self, 'userapoderado'):
            apoderado_perfil = self.get_userapoderado
        return apoderado_perfil
    
    def get_inspector_perfil(self):
        inspector_perfil = None
        if hasattr(self, 'userinspector'):
            inspector_perfil = self.get_userinspector
        return inspector_perfil
    
    def get_auditor_perfil(self):
        auditor_perfil = None
        if hasattr(self, 'userauditor'):
            auditor_perfil = self.get_userauditor
        return auditor_perfil


# TODO: detallar atributos particulares de cada tipo de usuario
class UserAdmin(models.Model):
    user_useradmin = models.OneToOneField(User, on_delete=models.PROTECT)
    active_useradmin = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user_useradmin.first_name + ' ' + self.user_useradmin.last_name
    
    class Meta:
        ordering = ['user_useradmin']
        verbose_name = 'Usuario Tipo Administrador'
        verbose_name_plural = 'Usuarios Tipo Administrador'
        

class UserAlumno(models.Model):
    user_useralumno = models.OneToOneField(User, on_delete=models.PROTECT)
    active_useralumno = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user_useralumno.first_name + ' ' + self.user_useralumno.last_name
    
    class Meta:
        ordering = ['user_useralumno']
        verbose_name = 'Usuario Tipo Alumno'
        verbose_name_plural = 'Usuarios Tipo Alumno'


class UserProfesor(models.Model):
    user_userprof = models.OneToOneField(User, on_delete=models.PROTECT)
    active_userprof = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user_userprof.first_name + ' ' + self.user_userprof.last_name
    
    class Meta:
        ordering = ['user_userprof']
        verbose_name = 'Usuario Tipo Profesor'
        verbose_name_plural = 'Usuarios Tipo Profesor'


class UserAdministrativo(models.Model):
    user_useradministrativo = models.OneToOneField(User, on_delete=models.PROTECT)
    active_useradministrativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user_useradministrativo.first_name + ' ' + self.user_useradministrativo.last_name
    
    class Meta:
        ordering = ['user_useradministrativo']
        verbose_name = 'Usuario Tipo Administrativo'
        verbose_name_plural = 'Usuarios Tipo Administrativo'


class UserApoderado(models.Model):
    user_userapoderado = models.OneToOneField(User, on_delete=models.PROTECT)
    active_userapoderado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user_userapoderado.first_name + ' ' + self.user_userapoderado.last_name
    
    class Meta:
        ordering = ['user_userapoderado']
        verbose_name = 'Usuario Tipo Apoderado'
        verbose_name_plural = 'Usuarios Tipo Apoderado'


class UserInspector(models.Model):
    user_userinspector = models.OneToOneField(User, on_delete=models.PROTECT)
    active_userinspector = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user_userinspector.first_name + ' ' + self.user_userinspector.last_name
    
    class Meta:
        ordering = ['user_userinspector']
        verbose_name = 'Usuario Tipo Inspector'
        verbose_name_plural = 'Usuarios Tipo Inspector'


class UserAuditor(models.Model):
    user_userauditor = models.OneToOneField(User, on_delete=models.PROTECT)
    active_useradmin = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user_userauditor.first_name + ' ' + self.user_userauditor.last_name
    
    class Meta:
        ordering = ['user_userauditor']
        verbose_name = 'Usuario Tipo Auditor'
        verbose_name_plural = 'Usuarios Tipo Auditor'
