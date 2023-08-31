# Generated by Django 4.2.1 on 2023-05-28 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_tipousuario_profile_usertype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='userType',
        ),
        migrations.AddField(
            model_name='profile',
            name='userType',
            field=models.CharField(choices=[('Donante', 'Donante'), ('Paciente', 'Paciente')], default='Donante', max_length=30),
        ),
    ]