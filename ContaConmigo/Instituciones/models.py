from django.db import models
# Create your models here.

class Provincia(models.Model):
    nombreProvincia = models.CharField(max_length=255)

    def __str__(self):
        return f' {self.nombreProvincia}'

class Ciudad(models.Model):
    nombreCiudad = models.CharField(max_length=255)
    codigoPostal = models.IntegerField()
    idProvincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.idProvincia} - {self.nombreCiudad}'

class Instituciones(models.Model):
    nombreInstitucion = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255)
    idCiudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.idCiudad} - {self.nombreInstitucion}'