from django import forms


from core.usuarios import models


class UserCreateModelForm(forms.ModelForm):
    region = forms.ModelChoiceField(
            queryset=models.Region.objects.all(),
            label='Región',
            required=False
            )
    provincia = forms.ModelChoiceField(
        queryset=models.Provincia.objects.all(),
        label='Provincia',
        required=False
        )
    alumno = forms.ModelChoiceField(
        queryset= models.UserAlumno.objects.all(),
        label='Alumno',
        required=False
    )
    is_sostenedor = forms.BooleanField(
        label='Es sostenedor',
        required=False
    )
    class Meta:
        model = models.User
        fields = [
            'first_name',
            'snombre_user',
            'last_name',
            'apmat_user',
            'username',
            'run_user',
            'dv_user',
            'email',
            'celular_user',
            'direccion_user',
            'comuna_user',
            'foto_user',
            'fecha_nac_user',
            'is_admin',
            'is_alumno',
            'is_profesor',
            'is_administrativo',
            'is_apoderado',
            'is_inspector',
            'is_auditor',
        ]
        
        labels = {
            'first_name': 'Nombre',
            'snombre_user': 'Segundo Nombre',
            'last_name': 'Primer Apellido',
            'apmat_user': 'Segundo Apellido',
            'username': 'Username',
            'run_user': 'Run',
            'dv_user': 'Dv',
            'email': 'Email',
            'celular_user': 'Celular',
            'direccion_user': 'Dirección',
            'comuna_user': 'Comuna',
            'foto_user': 'Foto',
            'fecha_nac_user': 'Fecha Nacimiento',
            'is_admin': 'Seleccionar si usuario es Administrador',
            'is_alumno': 'Seleccionar si usuario es Alumno',
            'is_profesor': 'Seleccionar si usuario es Profesor',
            'is_administrativo': 'Seleccionar si usuario es Administrativo',
            'is_apoderado': 'Seleccionar si usuario es Apoderado',
            'is_inspector': 'Seleccionar si usuario es Inspector',
            'is_auditor': 'Seleccionar si usuario es Auditor',
        }
        
        error_messages = {
            'run_user': {
                'unique': 'El Run ingresado ya existe en los registros'
            },
            'username': {
                'unique': 'El Username ingresado ya existe en los registros'
            },
            'email': {
                'unique': 'El Email ingresado ya existe en los registros'
            }
        }
        
        def clean(self):
            """ Esta función se sobrescribe con el fin de realizar la validación de run 
                ingresado por el usuario

            Raises:
                forms.ValidationError: _Levanta una excepción si el dv ingresado no corresponde al run_

            Returns:
                _dict_: _Diccionario con información del formulario validada_
            """
            cleaned_data = super().clean()
            run_user = cleaned_data['run_user']
            valor = 11 - sum([int(a) * int(b) for a, b in zip(str(run_user).zfill(8), '32765432')]) % 11
            dv_correcto = { 10: 'K', 11: '0'}.get(valor, str(valor))
            dv_ingresado = (cleaned_data['dv_user']).upper()
            if dv_correcto != dv_ingresado:
                raise forms.ValidationError('El Run ingresado no es correcto, verifique la información')
            return cleaned_data                        