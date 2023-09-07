from django.db import models
from django.contrib.auth.models import User
from PIL import Image


from datetime import date
from Instituciones.models import Ciudad, Instituciones
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile' #show how we want it to be displayed

    # Override the save method of the model
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path) # Open image

        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size) # Resize image
            img.save(self.image.path) # Save it again and override the larger image

class TipoSangre(models.Model):
    tipoSangre = models.CharField(max_length=255)
    def __str__(self):
        return f'{self.tipoSangre}'

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="") # Delete profile when user is deleted
    is_paciente = models.BooleanField(default=False)
    SEX_OPTIONS = ((SEX_FEMALE := "F", "Femenino"), (SEX_MALE := "M", "Masculino"), (SEX_UNSURE := "U", "No Informa"), (SEX_NOBINARY := "N", "No Binario"))
    TIPO_DOCUMENTO = ((DNI := "DNI", "DNI"), (LE := "LE", "LE"), (LC := "LC", "LC"))
    GRUPO_FACTOR = (
    (A_POS := "A+", "A+"), (A_NEG := "A-", "A-"), (O_POS := "0+", "0+"), (O_NEG := "0-", "0-"), (B_POS := "B+", "B+"),
    (AB_POS := "AB+", "AB+"))
    tipoDNI = models.CharField(max_length=255, choices=TIPO_DOCUMENTO, default=DNI)
    dni = models.CharField(max_length=255, null=True)
    sexo = models.CharField(max_length=1, choices=SEX_OPTIONS, default=SEX_UNSURE)
    tipoSangre = models.CharField(max_length=255, choices=GRUPO_FACTOR, null=True)
    fechaNacimiento = models.DateField(null=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True)
    telefono = models.CharField(max_length=255, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True,verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True,null=True,verbose_name="updated at")

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def edad_actual(self):
        """Calcular edad actual basado en fecha de nacimiento :return: int edad"""
        if self.fechaNacimiento:
            # Obtener fecha de hoy
            today = date.today()
            # Calcular Edad
            age = today.year - self.fechaNacimiento.year - (
                        (today.month, today.day) < (self.fechaNacimiento.month, self.fechaNacimiento.day))
            return age

        # Si no tiene fecha su edad es 0
        return 0

    @property
    def sexo_descripcion(self):
        if self.sexo == 'F':
            descripcion_sexo = 'Femenino'
        elif self.sexo == 'M':
            descripcion_sexo = 'Masculino'
        elif self.sexo == 'U':
            descripcion_sexo = 'No Informa'
        elif self.sexo == 'N':
            descripcion_sexo = 'No Binario'
        return descripcion_sexo


class PacienteInstitucion(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.SET_NULL, null=True)
    institucion = models.ForeignKey(Instituciones, on_delete=models.SET_NULL, null=True)
    cantidadDonantes = models.IntegerField(null=True)
    mail = models.CharField(max_length=255, null=True)
    completo = models.BooleanField(default=False)
    fechaLimite = models.DateField(null=True, blank=True, default=None)
    comentario = models.TextField(max_length=1024, null=True, blank=True)
    tiposSangre = models.ManyToManyField(TipoSangre, related_name="sangrePacientes")
    created_at = models.DateTimeField(auto_now_add=True, null=True,verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True,null=True,verbose_name="updated at")

    def __str__(self):
        return f'{self.paciente} {self.institucion}  {self.fechaLimite}'

class Donantes(models.Model):
    is_donante = models.BooleanField(default=False)
    user = models.ManyToManyField(User, related_name="UsuarioDonante")  # Delete profile when user is deleted
    #user = models.ManyToManyField(User)  # Delete profile when user is deleted
    GRUPO_FACTOR = (
    (A_POS := "A+", "A+"), (A_NEG := "A-", "A-"), (O_POS := "0+", "0+"), (O_NEG := "0-", "0-"), (B_POS := "B+", "B+"),
    (AB_POS := "AB+", "AB+"))
    fechaDonancionElegida = models.DateField()
    tipoSangre = models.CharField(max_length=255, choices=GRUPO_FACTOR, null=True)
    comentario = models.TextField(max_length=1024, null=True, blank=True)
    confirmacionAsistencia = models.BooleanField(default=False)
    pacienteInstitucion = models.ManyToManyField(PacienteInstitucion, related_name="donantePacienteInstitucion")
    agradecimiento = models.TextField(max_length=1024, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True,verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True,null=True,verbose_name="updated at")

    def __str__(self):
        return f'{self.fechaDonancionElegida} {self.user}  {self.tipoSangre} {self.pacienteInstitucion} {self.confirmacionAsistencia}'

