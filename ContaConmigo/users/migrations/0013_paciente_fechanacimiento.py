# Generated by Django 4.2.1 on 2023-06-21 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_tiposangre_paciente_dni_paciente_sexo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='fechaNacimiento',
            field=models.DateField(null=True),
        ),
    ]
