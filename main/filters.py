import django_filters

from .models import Cliente, Propiedad, Visita, Operacion, Propiedad_Precio, Casa, Departamento
from django_tables2.views import SingleTableMixin

from django.db import models
from django import forms

# Define cuales campos de los Modelos servirán para hacer busquedas en la BD, y el criterio con el cual se busque:
# si es nombres: si el resultado contiene la palabra, si es numeros: si es mayor,igual o menor


class FiltroCliente(django_filters.FilterSet):
    class Meta:
        model = Cliente
        fields = {
            'nombre': ['icontains'],
            'apellido': ['icontains'],

        }


class FiltroOperacion(django_filters.FilterSet):
    class Meta:
        model = Operacion
        fields = {
            'nombre': ['icontains'],
            'propiedad': ['exact'],
            'fecha': ['gt', 'lt'],
            'comprado_por': ['exact'],
            'vendido_por': ['exact'],
        }


class FiltroPropiedad_Precio(django_filters.FilterSet):
    class Meta:
        model = Propiedad_Precio
        fields = {
            'propiedad': ['exact'],
            'fecha': ['gt', 'lt'],

        }


class FiltroVisita(django_filters.FilterSet):
    class Meta:
        model = Visita
        fields = {
            'cliente': ['exact'],
            'propiedad': ['exact'],
            'fecha': ['gt', 'lt'],
            'agente': ['exact'],

        }


class FiltroPrecio(django_filters.FilterSet):
    class Meta:
        model = Propiedad_Precio
        fields = {
            'propiedad': ['exact'],
            'fecha': ['gt', 'lt'],
        }


class FiltroPropiedad(django_filters.FilterSet):
    class Meta:
        model = Propiedad
        fields = {
            'en_venta': ['exact'],
            'cliente': ['exact'],
            'localidad': ['icontains'],
            'partido': ['icontains'],
            'CP': ['exact'],
            'direccion': ['icontains'],
            'numero': ['exact'],
            'ambientes': ['lt'],
            'dormitorios': ['lt'],
            'banos': ['lt'],
            'superficie_total': ['gt', 'lt'],

        }


class FiltroCasa(django_filters.FilterSet):
    class Meta:
        model = Casa
        fields = {
            'en_venta': ['exact'],
            'cliente': ['exact'],
            'localidad': ['icontains'],
            'partido': ['icontains'],
            'CP': ['exact'],
            'direccion': ['icontains'],
            'numero': ['exact'],
            'ambientes': ['exact'],
            'dormitorios': ['exact'],
            'banos': ['exact'],
            'cant_plantas': ['exact'],
            'superficie_total': ['gt', 'lt'],

            'pileta': ['exact'],
            'barrio_privado': ['exact'],
        }


class FiltroDpto(django_filters.FilterSet):

    class Meta:
        model = Departamento
        fields = {
            'en_venta': ['exact'],
            'cliente': ['exact'],
            'localidad': ['icontains'],
            'partido': ['icontains'],
            'CP': ['exact'],
            'direccion': ['icontains'],
            'numero': ['exact'],
            'piso': ['exact'],
            'depto': ['exact'],
            'expensas': ['lt'],
            'ambientes': ['lt'],
            'dormitorios': ['lt'],
            'banos': ['lt'],
            'superficie_total': ['gt'],

            'encargado': ['exact'],
            'seguridad': ['exact'],
            'ascensores': ['gt'],

        }

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
        }
