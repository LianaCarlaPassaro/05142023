from django.contrib.auth.models import User
from django.db import models
from Instituciones.models import Instituciones

class TipoSangre(models.Model):
    GRUPO_FACTOR = (
    (A_POS := "A+", "A+"), (A_NEG := "A-", "A-"), (O_POS := "0+", "0+"), (O_NEG := "0-", "0-"), (B_POS := "B+", "B+"),
    (AB_POS := "AB+", "AB+"))
    tipoSangre = models.CharField(max_length=255, choices=GRUPO_FACTOR)
    def __str__(self):
        return f'{self.tipoSangre}'

class Publicacion(models.Model):
    idPaciente = models.ForeignKey(User, on_delete=models.CASCADE)
    institucion = models.ForeignKey(Instituciones,  on_delete=models.SET_NULL, null=True)
    fechaLimite = models.DateField()
    cantidadDonantes = models.IntegerField()
    comentario = models.TextField(max_length=1024, null=True, blank=True)
    completo = models.BooleanField(default=False)
    telefono = models.CharField(max_length=255)
    mail = models.CharField(max_length=255)
    tiposSangre = models.ManyToManyField(TipoSangre, related_name="sangrePacientes")
    createdBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='pacienteCreatedBy')
    modifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='pacienteModifiedBy')
    def __str__(self):
        return f'{self.idPaciente}  {self.institucion}'