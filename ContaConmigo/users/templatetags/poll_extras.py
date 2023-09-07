from django import template
from django.db import models
from ..models import Donantes

register = template.Library()


@register.filter(name='donantesAsistidos')
def cant_donantes_asistidos(value):
    var = 0
    donantes2 = Donantes.objects.filter(pacienteInstitucion__id=value, confirmacionAsistencia=True)
    for i in donantes2.all():
        var +=1
    return var

@register.filter(name='donantePostulado')
def donante_postulado(value, value1):
    boolean = False
    donantes = Donantes.objects.filter(pacienteInstitucion__id=value, confirmacionAsistencia=True)
    for don in donantes.all():
        if don.user_id == value1:
            boolean = True
    return boolean