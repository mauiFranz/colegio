# Generated by Django 4.0.6 on 2022-08-06 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0007_rename_alumno_apoderado_userapoderado_alumno_userapoderado_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='provincia',
            options={'ordering': ['region_provincia', 'codigo_provincia'], 'verbose_name': 'Provincia', 'verbose_name_plural': 'Provincias'},
        ),
    ]
