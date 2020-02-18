from django import forms
from .models import Cliente, Propiedad, Agente, Visita, Operacion, Telefono, Mail, Propiedad_Precio, Departamento, Casa

# Formularios de los Modelos creados, definiendo como se representarán graficamente sus campos.

class NuevoClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido']


class ClienteMailForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=30)
    apellido = forms.CharField(label='Apellido', max_length=30)
    mail = forms.EmailField()
    mail2 = forms.EmailField(required=False)
    telefono = forms.IntegerField(label='Numero')
    telefono2 = forms.IntegerField(label='Numero2', required=False)
    busca_ambientes = forms.IntegerField(label='Ambientes deseados', required=False)
    busca_precio = forms.IntegerField(label='Precio que busca', required=False)
    busca_localidad = forms.CharField(label='Localidad buscada', max_length=30, required=False)


class NuevaPropiedadForm(forms.ModelForm):
    class Meta:
        model = Propiedad
        fields = ['cliente', 'localidad', 'partido', 'CP', 'direccion', 'numero', 'entre', 'ambientes',
                  'dormitorios', 'banos', 'superficie_total', 'superficie_semicubierta', 'superficie_cubierta',
                  'superficie_descubierta', 'medida_frente', 'zonificacion', 'antiguedad', 'plano', 'orientacion',
                  'cochera', 'gas', 'cloacas', 'asfalto', 'agua_corriente', 'en_venta', 'apto_credito',
                  'apto_profesional', 'foto']


class NuevoDepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['cliente', 'localidad', 'partido', 'CP', 'direccion', 'numero', 'entre', 'piso', 'depto', 'expensas',
                  'ambientes', 'dormitorios', 'banos', 'cant_pisos', 'cant_dptos_por_piso', 'superficie_total',
                  'superficie_semicubierta', 'superficie_cubierta', 'superficie_descubierta', 'encargado',
                  'medida_frente', 'zonificacion', 'antiguedad', 'plano', 'orientacion', 'seguridad', 'cochera', 'gas',
                  'cloacas', 'asfalto', 'agua_corriente', 'en_venta', 'apto_credito', 'apto_profesional', 'balcon',
                  'ascensores', 'descripcion', 'vista', 'foto']


class NuevaCasaForm(NuevaPropiedadForm):
    class Meta:
        model = Casa

        fields = NuevaPropiedadForm.Meta.fields + ['cant_plantas', 'pileta', 'barrio_privado', 'descripcion']


class NuevoAgenteForm(forms.ModelForm):
    class Meta:
        model = Agente
        fields = ['nombre', 'apellido']


class NuevaVisitaForm(forms.ModelForm):
    fecha = forms.DateField(label='Fecha de Visita:', widget=forms.SelectDateWidget())

    class Meta:
        model = Visita
        fields = ['propiedad', 'cliente', 'agente', 'fecha', 'descripcion']


class NuevoMailForm(forms.ModelForm):
    class Meta:
        model = Mail
        fields = ['cliente', 'mail']


class NuevoTelForm(forms.ModelForm):
    class Meta:
        model = Telefono
        fields = ['cliente', 'numero']


class NuevaOperacionForm(forms.ModelForm):
    class Meta:
        model = Operacion
        fields = ['propiedad', 'vendido_por', 'comprado_por', 'monto', 'fecha', 'escribano', 'boleto', 'nombre']


class NuevoPrecioForm(forms.ModelForm):
    class Meta:
        model = Propiedad_Precio
        fields = ['propiedad', 'precio', 'fecha']
