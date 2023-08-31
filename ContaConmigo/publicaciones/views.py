from django.shortcuts import render
from .models import Publicacion, User
from django.http import HttpResponse

# Create your views here.

def index(request):
    context = {
        'Publicacions': Publicacion.objects.all()
    }
    return render(request, 'publicaciones/index.html', context)

def acercade(request):
    return render(request, 'publicaciones/acercade.html', {'title': 'AcercaDe'})

