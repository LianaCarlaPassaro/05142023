# Generated by Django 4.2.1 on 2023-05-17 03:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Instituciones', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoSangre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoSangre', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('0+', '0+'), ('0-', '0-'), ('B+', 'B+'), ('AB+', 'AB+')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaLimite', models.DateField()),
                ('cantidadDonantes', models.IntegerField()),
                ('comentario', models.TextField(blank=True, max_length=1024, null=True)),
                ('completo', models.BooleanField(default=False)),
                ('telefono', models.CharField(max_length=255)),
                ('mail', models.CharField(max_length=255)),
                ('createdBy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pacienteCreatedBy', to=settings.AUTH_USER_MODEL)),
                ('idPaciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('institucion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Instituciones.instituciones')),
                ('modifiedBy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pacienteModifiedBy', to=settings.AUTH_USER_MODEL)),
                ('tiposSangre', models.ManyToManyField(related_name='sangrePacientes', to='publicaciones.tiposangre')),
            ],
        ),
    ]
