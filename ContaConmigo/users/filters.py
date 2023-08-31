import django_filters
from .models import PacienteInstitucion
from django_filters import CharFilter


class PacienteFilter(django_filters.FilterSet):
    class Meta:
        model = PacienteInstitucion
        fields = ['institucion_id', 'tiposSangre']
        labels = {
            'tiposSangre': 'Tipos y Grupos Sanguíneos Solicitados',
            'institucion_id' : 'Institución'
        }
