# Generated by Django 4.2.3 on 2023-07-10 02:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_rename_fechareposicionelegida_donantes_fechadonancionelegida_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donantes',
            name='fechaConfirmacionAsistencia',
        ),
    ]
