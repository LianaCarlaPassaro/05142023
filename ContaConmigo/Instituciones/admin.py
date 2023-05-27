from django.contrib import admin
from .models import Instituciones, Provincia, Ciudad

# Register your models here.
admin.site.register(Instituciones)
admin.site.register(Ciudad)
admin.site.register(Provincia)