from django.shortcuts import redirect, render, HttpResponse
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from core.usuarios import models
from core.usuarios import forms



class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.CreateView):
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
        context['form_subtitle'] = 'Seleccione el Perfil Base del Usuario'
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
                    user_useradmin=usuario,
                    active_useradmin=True
                )
                usuario.perfil_base_user = 'is_admin'
                gpo_admin = Group.objects.get(name='gpo_admin')
                usuario.groups.add(gpo_admin)

            elif usuario.is_alumno:
                print('usuario alumno')
                alumno = models.UserAlumno.objects.create(
                    user_useralumno=usuario,
                    active_useralumno=True
                )
                usuario.perfil_base_user = 'is_alumno'
                gpo_alumno = Group.objects.get(name='gpo_alumno')
                usuario.groups.add(gpo_alumno)

            elif usuario.is_profesor:
                print('usuario profesor')
                profesor = models.UserProfesor.objects.create(
                    user_userprof=usuario,
                    active_userprof=True
                )
                usuario.perfil_base_user = 'is_profesor'
                gpo_profesor = Group.objects.get(name='gpo_profesor')
                usuario.groups.add(gpo_profesor)

            elif usuario.is_administrativo:
                print('usuario administrativo')
                administrativo = models.UserAdministrativo.objects.create(
                    user_useradministrativo=usuario,
                    active_useradministrativo=True
                )
                usuario.perfil_base_user = 'is_administrativo'
                gpo_administrativo = Group.objects.get(
                    name='gpo_administrativo')
                usuario.groups.add(gpo_administrativo)

            elif usuario.is_apoderado:
                alumno = form.cleaned_data['alumno']
                is_sostenedor = form.cleaned_data['is_sostenedor']
                apoderado = models.UserApoderado.objects.create(
                    user_userapoderado=usuario,
                    active_userapoderado=True,
                    alumno_userapoderado=alumno,
                    es_sostenedor_userapoderado=is_sostenedor
                )
                usuario.perfil_base_user = 'is_apoderado'
                gpo_apoderado = Group.objects.get(name='gpo_apoderado')
                usuario.groups.add(gpo_apoderado)

            elif usuario.is_inspector:
                print('usuario inspector')
                inspector = models.UserInspector.objects.create(
                    user_userinspector=usuario,
                    active_userinspector=True
                )
                usuario.perfil_base_user = 'is_inspector'
                gpo_inspector = Group.objects.get(name='gpo_inspector')
                usuario.groups.add(gpo_inspector)

            elif usuario.is_auditor:
                print('usuario auditor')
                auditor = models.UserAuditor.objects.create(
                    user_userauditor=usuario,
                    active_userauditor=True,
                )
                usuario.perfil_base_user = 'is_auditor'
                gpo_auditor = Group.objects.get(name='gpo_auditor')
                usuario.groups.add(gpo_auditor)

            print(usuario.get_all_permissions())
            usuario.save()
            messages.success(request, 'Usuario creado correctamente')
            return redirect('usuarios:list')
        else:
            return render(request, 'core/usuarios/create.html', {'form': form})


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.UpdateView):
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
    paginate_by = 5  # TODO: cambiar
    template_name = 'core/usuarios/list.html'
    permission_required = ['usuarios.view_user']
    permission_denied_message = 'No posee los permisos necesarios para acceder a esta información'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Usuarios'
        context['table_title'] = 'Listado de Usuarios Registrados'
        return context


class UserDeleteView(SuccessMessageMixin, generic.DeleteView):
    model = models.User
    template_name = 'core/usuarios/delete.html'
    success_url = reverse_lazy('usuarios:list')

    def post(self, request, pk, *args, **kwargs):
        instancia = self.model.objects.get(pk=pk)
        if instancia.is_admin:
            print('usuario admin')
            admin = models.UserAdmin.objects.get(user_useradmin=instancia)
            admin.active_useradmin = False
            admin.save()

        elif instancia.is_alumno:
            print('usuario alumno')
            alumno = models.UserAlumno.objects.get(user_useralumno=instancia)
            alumno.active_useralumno = False
            alumno.save()

        elif instancia.is_profesor:
            print('usuario profesor')
            profesor = models.UserProfesor.objects.get(user_userprof=instancia)
            profesor.active_userprof = False
            profesor.save()

        elif instancia.is_administrativo:
            print('usuario administrativo')
            administrativo = models.UserAdministrativo.objects.get(
                user_useradministrativo=instancia)
            administrativo.active_useradministrativo = False
            administrativo.save()

        elif instancia.is_apoderado:
            apoderado = models.UserApoderado.objects.get(
                user_userapoderado=instancia)
            apoderado.active_userapoderado = False
            apoderado.save()

        elif instancia.is_inspector:
            print('usuario inspector')
            inspector = models.UserInspector.objects.get(
                user_userinspector=instancia)
            inspector.active_userinspector = False
            inspector.save()

        elif instancia.is_auditor:
            print('usuario auditor')
            auditor = models.UserAuditor.objects.get(
                user_userauditor=instancia)
            auditor.active_userauditor = False
            auditor.save()

        instancia.save()
        return redirect('usuarios:list')


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


class RolesUpdateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    model = models.User
    template_name = 'core/usuarios/perfiles.html'
    form_class = forms.PerfilesModelForm
    success_url = reverse_lazy('usuarios:list')
    permission_required = ['usuarios.view_user', 'usuarios.change_user']
    permission_denied_message = 'No posee los permisos necesarios para realizar esta acción'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Usuarios'
        context['form_title'] = 'Actualización de Perfiles de Usuario'
        return context

    def get(self, request, *args, **kwargs):
        form = forms.RunSearchForm()
        context = {
            'form': form,
            'title': 'Usuarios',
            'form_title': 'Ingrese el Run del usuario a buscar',
            'form_subtitle': 'Seleccione los perfiles que desea asignar al usuario'
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        """ Esta función recibe los nuevos perfiles que deben ser asignados al usuario,
            cada usuario posee un pefil base que puede ser compatible con algunos otros.
            Antes de realizar cualquier cambio, se debe validar que los perfiles
            seleccionados por sean compatibles, una vez validados se deben asignar
            eliminando los antiguos permisos

        """
        print(f'views.py => line 261 => request.POST == {request.POST}')
        if request.POST['search'] == 'user':
            run = request.POST['run']
            form = forms.RunSearchForm()
            context = {
                'form': form,
                'title': 'Usuarios',
                'form_title': 'Ingrese el Run del usuario a buscar',
                'form_subtitle': 'Seleccione los perfiles que desea asignar al usuario'
            }
            if not run:
                return render(request, self.template_name, context)

            else:
                usuario = models.User.objects.filter(run_user=run).first()
                if usuario:
                    form = forms.PerfilesModelForm(instance=usuario)
                    context = {
                        'user_encontrado': usuario,
                        'title': 'Usuarios',
                        'form': form,
                        'form_title': 'Seleccione los perfiles que desea asignar al usuario'
                    }
                    return render(request, self.template_name, context)
                else:
                    extra_tags = {
                        'title': 'Atención',
                        'icon': 'warning',
                        'confirmButtonText': 'Cerrar',

                    }
                    messages.warning(
                        request, 'No existe un usuario con el Run ingresado', extra_tags=extra_tags)
                    return render(request, self.template_name, context)
        else:

            # Lista para almacenar los perfiles de usuario seleccionados
            perfiles_disponibles = ['is_admin', 'is_administrativo', 'is_alumno',
                'is_apoderado', 'is_auditor', 'is_inspector', 'is_profesor']
            perfiles_nuevos = []
            perfiles_antiguos = []
            usuario = None

            # Se recupera el usuario que se está modificando
            formulario = forms.PerfilesModelForm(request.POST)
            usuario = self.model.objects.filter(pk=request.POST['user']).first()
            perfil_defecto = usuario.perfil_base_user

            # Obtener lista de perfiles antiguos
            perfiles_antiguos = usuario.get_all_perfiles_vigentes()
            print(f'views.py => line 310 => request == {request.POST}')            
            print(f'views.py => line 311 => perfiles_antiguos == {perfiles_antiguos}')
            for param in request.POST:
                # Se quita to token del formulario de la lista
                if param != 'csrfmiddlewaretoken':
                    perfiles_nuevos.append(param)

            try:
                perfiles_nuevos.remove('user')
                perfiles_nuevos.remove('alumno')
                perfiles_nuevos.remove('search')
                perfiles_nuevos.remove(perfil_defecto)
                
            except:
                form = forms.PerfilesModelForm(instance=usuario)
                context = {
                    'user_encontrado': usuario,
                    'title': 'Usuarios',
                    'form': form,
                    'form_title': 'Seleccione los perfiles que desea asignar al usuario'
                }
                extra_tags = {
                    'title': 'Atención',
                    'icon': 'error',
                    'confirmButtonText': 'Cerrar',

                }
                messages.success(request, 'El perfil por defecto no se puede eliminar', extra_tags=extra_tags)
                return render(request, self.template_name, context=context)
                    
            print(
                f'views.py => line => 305 => perfiles_nuevos {perfiles_nuevos}')

            # Se comprueba si la nueva lista de perfiles es compatible con el perfil por defecto
            lista_compatibles = usuario.get_perfiles_compatibles()
            mensage_retorno = 'Los sigientes perfiles no se pudieron asignar, ya que no son compatibles con el perfil base del usuario: '
            perfiles_no_compatibles = 0
            for perfil in perfiles_disponibles:
                print(f'views.py => line 312 => perfil == {perfil}')
                if perfil == usuario.perfil_base_user:
                    print(f'views.py => line 312 => perfil es igual a base == {perfil}')
                    continue

                elif perfil in perfiles_nuevos and perfil in perfiles_antiguos:
                    print(f'views.py => line 312 => perfil es nuevo y antiguo == {perfil}')
                    continue

                elif perfil in perfiles_nuevos:
                    print(f'views.py => line 312 => perfil es nuevo == {perfil}')

                    if perfil in lista_compatibles:
                        print(f'views.py => line 312 => perfil es nuevo y compatible == {perfil}')

                        if perfil == 'is_admin':
                            print('usuario admin')
                            admin = models.UserAdmin.objects.create(
                                 user_useradmin=usuario,
                                 active_useradmin=True
                            )
                            usuario.is_admin = True
                            gpo_admin = Group.objects.get(name='gpo_admin')
                            usuario.groups.add(gpo_admin)
                          
                        elif perfil == 'is_alumno':
                            print('usuario alumno')
                            alumno = models.UserAlumno.objects.create(
                                user_useralumno = usuario,
                                active_useralumno = True
                            )
                            usuario.is_alumno = True
                            gpo_alumno = Group.objects.get(name='gpo_alumno')
                            usuario.groups.add(gpo_alumno)
                        
                        elif perfil == 'is_profesor':
                            print('usuario profesor')
                            profesor = models.UserProfesor.objects.create(
                                user_userprof = usuario,
                                active_userprof = True
                            )
                            usuario.is_profesor = True
                            gpo_profesor = Group.objects.get(name='gpo_profesor')
                            usuario.groups.add(gpo_profesor)
                        
                        elif perfil == 'is_administrativo':
                            print('usuario administrativo')
                            administrativo = models.UserAdministrativo.objects.create(
                                user_useradministrativo = usuario,
                                active_useradministrativo = True
                            )
                            usuario.is_administrativo = True
                            gpo_administrativo = Group.objects.get(name='gpo_administrativo')
                            usuario.groups.add(gpo_administrativo)
                           
                        elif perfil == 'is_apoderado':
                            # TODO: Corregir problemas al almacenar este perfil
                            alumno = self.model.objects.filter(pk=request.POST['alumno']).first()
                            user_alumno = alumno.get_alumno_perfil()
                            print(f'views.py => line 406 => alumno == {user_alumno}')
                            try:
                                request.POST['is_sostenedor']
                                is_sostenedor = True
                            except:
                                is_sostenedor = False
                            apoderado = models.UserApoderado.objects.create(
                                user_userapoderado = usuario,
                                active_userapoderado = True,
                                alumno_userapoderado = user_alumno,
                                es_sostenedor_userapoderado = is_sostenedor
                            )
                            usuario.is_apoderado = True
                            gpo_apoderado = Group.objects.get(name='gpo_apoderado')
                            usuario.groups.add(gpo_apoderado)
                        
                        elif perfil == 'is_inspector':
                            print('usuario inspector')
                            inspector = models.UserInspector.objects.create(
                                user_userinspector = usuario,
                                active_userinspector = True
                            )
                            usuario.is_inspector = True
                            gpo_inspector = Group.objects.get(name='gpo_inspector')
                            usuario.groups.add(gpo_inspector)
                        
                        elif perfil == 'is_auditor':
                            print('usuario auditor')
                            auditor = models.UserAuditor.objects.create(
                                user_userauditor = usuario,
                                active_userauditor = True,
                            )
                            usuario.is_auditor = True
                            gpo_auditor = Group.objects.get(name='gpo_auditor')
                            usuario.groups.add(gpo_auditor)
                        continue
                    
                    else:
                        print(f'views.py => line 312 => perfil es nuevo y no compatible == {perfil}')
                        mensage_retorno += str(perfil[3:]).capitalize() + ', '
                        perfiles_no_compatibles += 1
                        continue
                    
                elif perfil in perfiles_antiguos:
                    print(f'views.py => line 312 => perfil es antiguo == {perfil}')
                    
                    if perfil == 'is_admin':
                        print('usuario admin')
                        admin = usuario.get_admin_perfil()
                        admin.delete()
                        usuario.is_admin = False
                        gpo_admin = Group.objects.get(name='gpo_admin')
                        usuario.groups.remove(gpo_admin)
                        
                    elif perfil == 'is_alumno':
                        print('usuario alumno')
                        alumno = usuario.get_alumno_perfil()
                        alumno.delete()
                        usuario.is_alumno = False
                        gpo_alumno = Group.objects.get(name='gpo_alumno')
                        usuario.groups.remove(gpo_alumno)
                        
                    elif perfil == 'is_profesor':
                        print('usuario profesor')
                        profesor = usuario.get_profesor_perfil()
                        profesor.delete()
                        usuario.is_profesor = False
                        gpo_profesor = Group.objects.get(name='gpo_profesor')
                        usuario.groups.remove(gpo_profesor)
                        
                    elif perfil == 'is_administrativo':
                        print('usuario administrativo')
                        administrativo = usuario.get_administrativo_perfil()
                        administrativo.delete()
                        usuario.is_administrativo = False
                        gpo_administrativo = Group.objects.get(name='gpo_administrativo')
                        usuario.groups.remove(gpo_administrativo)
                        
                    elif perfil == 'is_apoderado':
                        apoderado = usuario.get_apoderado_perfil()
                        apoderado.delete()
                        usuario.is_apoderado = False
                        gpo_apoderado = Group.objects.get(name='gpo_apoderado')
                        usuario.groups.remove(gpo_apoderado)
                        
                    elif perfil == 'is_inspector':
                        print('usuario inspector')
                        inspector = usuario.get_inspector_perfil()
                        inspector.delete()
                        usuario.is_inspector = False
                        gpo_inspector = Group.objects.get(name='gpo_inspector')
                        usuario.groups.remove(gpo_inspector)
                        
                    elif perfil == 'is_auditor':
                        print('usuario auditor')
                        auditor = usuario.get_auditor_perfil()
                        auditor.delete()
                        usuario.is_auditor = False
                        gpo_auditor = Group.objects.get(name='gpo_auditor')
                        usuario.groups.remove(gpo_auditor)

                    continue
                usuario.save()
                
            form = forms.RunSearchForm()
            context = {
                'form': form,
                'title': 'Usuarios',
                'form_title': 'Ingrese el Run del usuario a buscar',
                'form_subtitle': 'Seleccione los perfiles que desea asignar al usuario'
            }
            extra_tags = {
                'title': 'Atención',
                'icon': 'success',
                'confirmButtonText': 'Cerrar',

            }
            if perfiles_no_compatibles > 0:
                messages.info(request, f'¡Perfiles actualizados con observaciones¡. {mensage_retorno}', extra_tags=extra_tags)
            
            else:
                messages.success(request, f'¡Perfiles compatibles actualizados con exito!', extra_tags=extra_tags)
                
            return render(request, self.template_name, context=context)


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
    
    


















