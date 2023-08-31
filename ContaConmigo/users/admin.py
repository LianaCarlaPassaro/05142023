from django.contrib import admin
from .models import Profile, Paciente, PacienteInstitucion,Donantes
# Register your models here.
admin.site.register(Profile)
admin.site.register(Paciente)
admin.site.register(PacienteInstitucion)
admin.site.register(Donantes)
