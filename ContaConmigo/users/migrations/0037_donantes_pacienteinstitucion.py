# Generated by Django 4.2.3 on 2023-07-15 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0036_remove_donantes_pacienteinstitucion'),
    ]

    operations = [
        migrations.AddField(
            model_name='donantes',
            name='pacienteInstitucion',
            field=models.ManyToManyField(related_name='donantePacienteInstitucion', to='users.pacienteinstitucion'),
        ),
    ]
