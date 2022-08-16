from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
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
        ordering = ['region_provincia', 'codigo_provincia']
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


class UserManager(BaseUserManager):
    def _create_user(self,  username, email, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            email = email,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_user(self,  username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)
    
    def create_superuser(self,  username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, True, True, **extra_fields)
    

class User(AbstractUser):
    """ Clase abstracta que unifica la funcionalidad y atributos de todos los usuarios
        reemplaza al usuario básico de django
    """
    PERFILES_BASE = [
        ('is_admin', 'Administrador'),
        ('is_administrativo', 'Administrativo'),
        ('is_alumno', 'Alumno'),
        ('is_apoderado', 'Apoderado'),
        ('is_auditor', 'Auditor'),
        ('is_inspector', 'Inspector'),
        ('is_profesor', 'Profesor')
    ]
    run_user = models.PositiveIntegerField(unique=True, verbose_name='RUN')
    dv_user = models.CharField(max_length=1, verbose_name='DV')
    snombre_user = models.CharField(max_length=25, null=True, blank=True, verbose_name='Segundo Nombre')
    apmat_user = models.CharField(max_length=25, null=True, blank=True, verbose_name='Apellido Materno')
    celular_user = models.IntegerField(unique=True, null=True, blank=True, verbose_name='Celular')
    direccion_user = models.CharField(max_length=100, null=True, blank=True, verbose_name='Dirección')
    comuna_user = models.ForeignKey(Comuna, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Comuna')
    foto_user = models.ImageField(upload_to='uploads/fotos/', null=True, blank=True, validators=[FileExtensionValidator(['png'])])
    fecha_nac_user = models.DateField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_alumno = models.BooleanField(default=False)
    is_profesor = models.BooleanField(default=False)
    is_administrativo = models.BooleanField(default=False)
    is_apoderado = models.BooleanField(default=False)
    is_inspector = models.BooleanField(default=False)
    is_auditor = models.BooleanField(default=False)
    perfil_base_user = models.CharField(max_length=20, choices=PERFILES_BASE, verbose_name='Perfil Base')
    objects = UserManager()
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    class Meta:
        db_table = 'auth_user'
        ordering = ['username']
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    REQUIRED_FIELDS = ['run_user', 'dv_user', 'email']
        
    def get_admin_perfil(self):
        admin_perfil = None
        if hasattr(self, 'useradmin'):
            admin_perfil = self.get_useradmin
        return admin_perfil
    
    def get_alumno_perfil(self):
        alumno_perfil = None
        if hasattr(self, 'useralumno'):
            alumno_perfil = self.useralumno
        return alumno_perfil
    
    def get_profesor_perfil(self):
        profesor_perfil = None
        if hasattr(self, 'userprof'):
            profesor_perfil = self.userprofesor
        return profesor_perfil
            
    def get_administrativo_perfil(self):
        administrativo_perfil = None
        if hasattr(self, 'useradministrativo'):
            administrativo_perfil = self.useradministrativo
        return administrativo_perfil
    
    def get_apoderado_perfil(self):
        apoderado_perfil = None
        if hasattr(self, 'userapoderado'):
            apoderado_perfil = self.userapoderado
        return apoderado_perfil
    
    def get_inspector_perfil(self):
        inspector_perfil = None
        if hasattr(self, 'userinspector'):
            inspector_perfil = self.userinspector
        return inspector_perfil
    
    def get_auditor_perfil(self):
        auditor_perfil = None
        if hasattr(self, 'userauditor'):
            auditor_perfil = self.userauditor
        return auditor_perfil
    
    def get_perfiles_compatibles(self):
        """ Esta función valida que los perfiles que se desean asignar son compatibles
            con el perfil base asignado al usuario

        Args:
            perfiles (list, optional): _Lista con perfiles a asignar_. Defaults to [].

        Returns:
            _Boolean_: _True si los nuevos perfiles son compatibles, False en caso contrario_
        """
        compatibles = []
        if self.perfil_base_user == 'is_admin':
            compatibles = ['is_admin', 'is_administrativo', 'is_inspector']
            
        elif self.perfil_base_user == 'is_administrativo':
            compatibles = ['is_admin', 'is_administrativo', 'is_profesor', 'is_apoderado', 'is_inspector']
            
        elif self.perfil_base_user == 'is_inspector':
            compatibles = ['is_admin', 'is_profesor', 'is_administrativo', 'is_apoderado', 'is_inspector']
            
        elif self.perfil_base_user == 'is_profesor':
            compatibles = ['is_admin', 'is_administrativo', 'is_apoderado', 'is_inspector', 'is_profesor']
        
        return compatibles            

    def get_all_perfiles_vigentes(self):
        perfiles = []
        if self.is_admin and self.perfil_base_user != 'is_admin':
            perfiles.append('is_admin')
            
        if self.is_administrativo and self.perfil_base_user != 'is_administrativo':
            perfiles.append('is_administrativo')
            
        if self.is_alumno and self.perfil_base_user != 'is_alumno':
            perfiles.append('is_alumno')
            
        if self.is_apoderado and self.perfil_base_user != 'is_apoderado':
            perfiles.append('is_apoderado')
            
        if self.is_auditor and self.perfil_base_user != 'is_auditor':
            perfiles.append('is_auditor')
            
        if self.is_inspector and self.perfil_base_user != 'is_inspector':
            perfiles.append('is_inspector')
            
        if self.is_profesor and self.perfil_base_user != 'is_profesor':
            perfiles.append('is_profesor')
        return perfiles
    
    def delete_admin_perfil(self):
        if hasattr(self, 'useradmin'):
            admin_perfil = self.useradmin
            admin_perfil.delete()
            return True
        return False





# TODO: detallar atributos particulares de cada tipo de usuario
class UserAdmin(models.Model):
    user_useradmin = models.OneToOneField(User, on_delete=models.CASCADE)
    active_useradmin = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user_useradmin.first_name + ' ' + self.user_useradmin.last_name
    
    class Meta:
        ordering = ['user_useradmin']
        verbose_name = 'Usuario Tipo Administrador'
        verbose_name_plural = 'Usuarios Tipo Administrador'
        

class UserAlumno(models.Model):
    user_useralumno = models.OneToOneField(User, on_delete=models.CASCADE)
    active_useralumno = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user_useralumno.first_name + ' ' + self.user_useralumno.last_name
    
    class Meta:
        ordering = ['user_useralumno']
        verbose_name = 'Usuario Tipo Alumno'
        verbose_name_plural = 'Usuarios Tipo Alumno'


class UserProfesor(models.Model):
    user_userprof = models.OneToOneField(User, on_delete=models.CASCADE)
    active_userprof = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user_userprof.first_name + ' ' + self.user_userprof.last_name
    
    class Meta:
        ordering = ['user_userprof']
        verbose_name = 'Usuario Tipo Profesor'
        verbose_name_plural = 'Usuarios Tipo Profesor'


class UserAdministrativo(models.Model):
    user_useradministrativo = models.OneToOneField(User, on_delete=models.CASCADE)
    active_useradministrativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user_useradministrativo.first_name + ' ' + self.user_useradministrativo.last_name
    
    class Meta:
        ordering = ['user_useradministrativo']
        verbose_name = 'Usuario Tipo Administrativo'
        verbose_name_plural = 'Usuarios Tipo Administrativo'


class UserApoderado(models.Model):
    user_userapoderado = models.OneToOneField(User, on_delete=models.CASCADE)
    active_userapoderado = models.BooleanField(default=True)
    alumno_userapoderado = models.ForeignKey(UserAlumno, on_delete=models.DO_NOTHING)
    es_sostenedor_userapoderado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user_userapoderado.first_name + ' ' + self.user_userapoderado.last_name
    
    class Meta:
        ordering = ['user_userapoderado']
        verbose_name = 'Usuario Tipo Apoderado'
        verbose_name_plural = 'Usuarios Tipo Apoderado'


class UserInspector(models.Model):
    user_userinspector = models.OneToOneField(User, on_delete=models.CASCADE)
    active_userinspector = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user_userinspector.first_name + ' ' + self.user_userinspector.last_name
    
    class Meta:
        ordering = ['user_userinspector']
        verbose_name = 'Usuario Tipo Inspector'
        verbose_name_plural = 'Usuarios Tipo Inspector'


class UserAuditor(models.Model):
    user_userauditor = models.OneToOneField(User, on_delete=models.CASCADE)
    active_userauditor = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user_userauditor.first_name + ' ' + self.user_userauditor.last_name
    
    class Meta:
        ordering = ['user_userauditor']
        verbose_name = 'Usuario Tipo Auditor'
        verbose_name_plural = 'Usuarios Tipo Auditor'
