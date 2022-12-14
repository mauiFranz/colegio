# Generated by Django 4.0.6 on 2022-08-14 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0011_rename_active_useradmin_userauditor_active_userauditor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='perfil_base_user',
            field=models.CharField(choices=[('is_admin', 'Administrador'), ('is_administrativo', 'Administrativo'), ('is_alumno', 'Alumno'), ('is_apoderado', 'Apoderado'), ('is_auditor', 'Auditor'), ('is_inspector', 'Inspector'), ('is_profesor', 'Profesor')], max_length=20, verbose_name='Perfil Base'),
        ),
    ]
