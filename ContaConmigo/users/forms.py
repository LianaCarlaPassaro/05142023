from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta

from .models import Profile, User, Paciente, TipoSangre, PacienteInstitucion,Donantes


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    # Configuration
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Email',
            'password1': 'Contraseña',
            'password2': 'Re-ingrese la Contraseña'
        }

# Create a UserUpdateForm to update a username and email
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Email'
        }

# Create a ProfileUpdateForm to update image.
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        labels = {
            'image': 'Imagen',

        }

class TiposSangreForm(forms.ModelForm):
    class Meta:
        model = TipoSangre
        fields = ['tipoSangre']

class DateInput(forms.DateInput):
    input_type = 'date'

class DonanteReposicionForm(forms.ModelForm):
    class Meta:
        model = Donantes
        widgets = {'fechaDonancionElegida': DateInput()}
        fields = ['fechaDonancionElegida', 'tipoSangre', 'comentario']
        labels = {'fechaDonancionElegida': 'Fecha de Reposición Elegida:',
                  'tipoSangre': '¿Cuál es tu tipo de Sangre? '}
    def clean_fechaDonancionElegida(self):
        data = self.cleaned_data['fechaDonancionElegida']

        # Check if a date is not in the past.
        if data < date.today():
            raise ValidationError(_('Fecha Inválida - La fecha es pasada'))
        # Check if a date is in the allowed range (+4 weeks from today).
        if data > date.today() + timedelta(weeks=1):
            raise ValidationError(_('Fecha Inválida - Selecciona una fecha menor a 1 semana'))
        if self.confirmacionAsistencia ==False:
            raise ValidationError(_('bla'))
        # Remember to always return the cleaned data.
        return data



class nuevoPacienteInstitucionForm(forms.ModelForm):
    class Meta:
        model = PacienteInstitucion
        fields = ['institucion', 'mail', 'cantidadDonantes', 'fechaLimite', 'comentario', 'tiposSangre']
        labels = {
            'cantidadDonantes': 'Cantidad de Donantes Necesarios',
            'mail': 'Email Paciente',
            'fechaLimite': 'Fecha límite para Recepción de Donantes',
            'comentario': 'Comentarios',
            'tiposSangre': 'Tipos y Grupos Sanguíneos Solicitados',
            'institucion': 'Institución Médica'
        }

class PacienteRegisterForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['id', 'tipoDNI', 'dni',  'telefono', 'sexo','tipoSangre','fechaNacimiento', 'ciudad']

        labels = {
            'tipoDNI': 'Tipo Documento',
            'dni': 'Nro. Documento',
            'telefono':'Teléfono',
            'sexo': 'Sexo',
            'tipoSangre': 'Tipo y Grupo Sanguíneo',
            'fechaNacimiento': 'Fecha de Nacimiento',
            'ciudad': 'Ciudad Procendencia de Paciente',
        }

