from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group

from core.usuarios import models
from core.usuarios import forms

# Create your views here.
# CRUD user
class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin,  generic.CreateView):
    """ Esta clase permite la creación de usuarios, y del perfil que se
        le asigne

    """
    model = models.User
    form_class = forms.UserCreateModelForm
    template_name = 'core/usuarios/create.html'
    success_url = reverse_lazy('usuarios:list')
    permission_required = ['usuarios.view_user', 'usuarios.create_user']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Usuarios'
        context['form_title'] = 'Creación de Usuarios'
        context['form_subtitle'] = 'Seleccione el Perfil de Usuario'
        return context
    
    def post(self, request, *args, **kwargs):
        """ Este método sobrescribe al método post del createview
            se llama en cada petición post (crear un usuario)
            se le incorpora la funcionalidad para crear los perfiles relacionados
        """
        form = forms.UserCreateModelForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save()
            if usuario.is_admin:
                print('usuario admin')
                admin = models.UserAdmin.objects.create(
                    user_useradmin = usuario,
                    active_useradmin = True
                )
                gpo_admin = Group.objects.get(name='gpo_admin')
                usuario.groups.add(gpo_admin)
                
            elif usuario.is_alumno:
                print('usuario alumno')
                alumno = models.UserAlumno.objects.create(
                    user_useralumno = usuario,
                    active_useralumno = True
                )
                gpo_alumno = Group.objects.get(name='gpo_alumno')
                usuario.groups.add(gpo_alumno)
                
            elif usuario.is_profesor:
                print('usuario profesor')
                profesor = models.UserProfesor.objects.create(
                    user_userprof = usuario,
                    active_userprof = True
                )
                gpo_profesor = Group.objects.get(name='gpo_profesor')
                usuario.groups.add(gpo_profesor)
                
            elif usuario.is_administrativo:
                print('usuario administrativo')
                administrativo = models.UserAdministrativo.objects.create(
                    user_useradministrativo = usuario,
                    active_useradministrativo = True
                )
                gpo_administrativo = Group.objects.get(name='gpo_administrativo')
                usuario.groups.add(gpo_administrativo)
                
            elif usuario.is_apoderado:
                alumno = form.cleaned_data['alumno']
                is_sostenedor = form.cleaned_data['is_sostenedor']
                apoderado = models.UserApoderado.objects.create(
                    user_userapoderado = usuario,
                    active_userapoderado = True,
                    alumno_userapoderado = alumno,
                    es_sostenedor_userapoderado = is_sostenedor
                )
                gpo_apoderado = Group.objects.get(name='gpo_apoderado')
                usuario.groups.add(gpo_apoderado)
                
            elif usuario.is_inspector:
                print('usuario inspector')
                inspector = models.UserInspector.objects.create(
                    user_userinspector = usuario,
                    active_userinspector = True
                )
                gpo_inspector = Group.objects.get(name='gpo_inspector')
                usuario.groups.add(gpo_inspector)
                
            elif usuario.is_auditor:
                print('usuario auditor')
                auditor = models.UserAuditor.objects.create(
                    user_userauditor = usuario,
                    active_userauditor = True,
                )
                gpo_auditor = Group.objects.get(name='gpo_auditor')
                usuario.groups.add(gpo_auditor)
                
            print(usuario.get_all_permissions())
            usuario.save()
            return redirect('usuarios:list')
        else:
            return render(request, 'core/usuarios/create.html', {'form': form})


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = models.User
    form_class = forms.UserUpdateModelForm
    template_name = 'core/usuarios/update.html'
    success_url = reverse_lazy('usuarios:list')
    permission_required = ['usuarios.view_user', 'usuarios.change_user']
    permission_denied_message = 'No posee los permisos necesarios para realizar esta acción'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Usuarios'
        context['form_title'] = 'Actualización de Usuarios'
        return context


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    """ Esta clase devuelve la lista de usuarios registrados
        TODO: definir queryset
    """
    model = models.User
    paginate_by = 5 # TODO: cambiar 
    template_name = 'core/usuarios/list.html'
    permission_required = ['usuarios.view_user']
    permission_denied_message = 'No posee los permisos necesarios para acceder a esta información'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Usuarios'
        context['table_title'] = 'Listado de Usuarios Registrados'
        return context


class UserDeleteView(generic.DeleteView):
    pass


class UserDetailView(generic.DetailView):
    model = models.User
    template_name = 'core/usuarios/detail.html'
    context_object_name = 'usuario'
    
    def get_object(self):
        obj = super().get_object()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_head'] = 'Usuarios'
        context['title_page'] = 'Perfil de Usuario'
        context['subtitle'] = ''
        return context
        


class RegionListView(generic.ListView):
    model = models.Region
    

class ProvinciaListView(generic.ListView):
    """ Se crea esta clase para llenar los select de los templates
        que requieran mostrar información de las provincias filtradas por alguna región
        (select's anidados)
    """
    model = models.Provincia
    template_name = 'core/usuarios/provincias_selectbox.html'
    context_object_name = 'provincias'
    http_method_names = ['get']
    
    def get_queryset(self):
        id_region = self.request.GET.get('id_region', None)
        if id_region:
            query = self.model.objects.filter(region_provincia_id=id_region)
        else:
            query = self.model.objects.all()
        return query
    
    
class ComunaListView(generic.ListView):
    """ Se crea esta clase para llenar los select de los templates
        que requieran mostrar información de las comunas filtradas por alguna 
        provincia (select's anidados)
    """
    model = models.Comuna
    template_name = 'core/usuarios/comunas_selectbox.html'
    context_object_name = 'comunas'
    http_method_names = ['get']
    
    def get_queryset(self):
        id_provincia = self.request.GET.get('id_provincia', None)
        if id_provincia:
            query = self.model.objects.filter(provincia_comuna_id=id_provincia)
        else:
            query = self.model.objects.all()
        return query