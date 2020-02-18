from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.

#Clientes de la inmobiliaria
class Cliente(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)

    #Criterio opcional basico de busqueda del cliente
    busca_ambientes = models.PositiveIntegerField(null=True, blank=True, default=1)
    busca_precio = models.PositiveIntegerField(null=True, blank=True, default=1)
    busca_localidad = models.CharField(max_length=30, null=True, blank=True, default='San Miguel')

    class Meta:
        verbose_name_plural = "clientes"

    # Esto define la representación del objeto.
    def __str__(self):
        return '%s %s' % (self.nombre, self.apellido)

    def get_absolute_url(self):
        return reverse("main:home")

# Un Cliente puede tener muchos Telefonos
class Telefono(models.Model):
    numero = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.numero)


# Un Cliente puede tener muchos Mails
class Mail(models.Model):
    mail = models.CharField(max_length=30)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return self.mail


def upload_location(instance, filename):
    return "%s %s/%s" % (instance.direccion, instance.numero, filename)


# Clase base de las Propiedades
class Propiedad(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    en_venta = models.BooleanField(blank=True)
    apto_credito = models.BooleanField()
    apto_profesional = models.BooleanField()
    CP = models.PositiveIntegerField()
    localidad = models.CharField(max_length=30)
    partido = models.CharField(max_length=30)
    direccion = models.CharField(max_length=30)
    entre = models.CharField(max_length=70, blank=True)
    numero = models.PositiveIntegerField()

    antiguedad = models.PositiveIntegerField(blank=True)
    plano = models.BooleanField()

    superficie_total = models.PositiveIntegerField()
    superficie_semicubierta = models.PositiveIntegerField()
    superficie_cubierta = models.PositiveIntegerField()
    superficie_descubierta = models.PositiveIntegerField()
    medida_frente = models.PositiveIntegerField(blank=True, default='')
    ambientes = models.PositiveIntegerField()
    dormitorios = models.PositiveIntegerField()
    banos = models.PositiveIntegerField()

    cochera = models.BooleanField()
    gas = models.BooleanField(blank=True)
    cloacas = models.BooleanField(blank=True)
    asfalto = models.BooleanField(blank=True)
    agua_corriente = models.BooleanField(blank=True)

    foto = models.ImageField(upload_to=upload_location, blank=True, null=True)

    publicada = models.DateField(default=timezone.now)
    descripcion = models.TextField(max_length=300, default='', blank=True)

    orientaciones = (
        ('n', 'Nor'),
        ('s', 'Sur'),
        ('e', 'Este'),
        ('o', 'Oeste'),
        ('no', 'Noroeste'),
        ('so', 'Sudoeste'),
    )

    zonificaciones = (
        ('u', 'Urbana'),
        ('r', 'Rural'),
        ('s', 'Semiurbana'),
    )

    # Atributos con multiple choice
    orientacion = models.CharField(max_length=1, choices=orientaciones, blank=True, default='s',
                                   help_text='Orientacion del Inmueble')

    zonificacion = models.CharField(max_length=1, choices=zonificaciones, blank=True, default='c',
                                    help_text='Zonificacion del Inmueble')

    # Esto define el nombre cuando sea plural
    class Meta:
        verbose_name_plural = "propiedades"

    # Esto define la representación del objeto.
    def __str__(self):
        return '%s %s' % (self.direccion, self.numero)

    def get_absolute_url(self):
        return reverse("main:home")


# Clase heredada de Propiedad
class Departamento(Propiedad):
    piso = models.PositiveIntegerField()
    depto = models.CharField(max_length=3, blank=True)
    expensas = models.PositiveIntegerField()
    cant_pisos = models.PositiveIntegerField(blank=True)
    cant_dptos_por_piso = models.PositiveIntegerField(blank=True)
    encargado = models.BooleanField(blank=True)
    seguridad = models.BooleanField(blank=True)
    balcon = models.BooleanField()
    ascensores = models.PositiveIntegerField()

    vistas = (
        ('f', 'Frente'),
        ('c', 'Contrafrente'),
        ('l', 'Lateral'),
        ('i', 'Interno'),
    )

    vista = models.CharField(max_length=1, choices=vistas, blank=True, default='c',
                             help_text='Vista del Inmueble')


# Clase heredada de Propiedad
class Casa(Propiedad):
    cant_plantas = models.PositiveIntegerField(blank=True)
    pileta = models.BooleanField(blank=True)
    barrio_privado = models.BooleanField(blank=True)


# Precio de una Propiedad en una fecha dada
class Propiedad_Precio(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    precio = models.IntegerField()
    fecha = models.DateTimeField(default=timezone.now)

    # Esto define la representación del objeto.
    def __str__(self):
        return self.propiedad.direccion + str(self.propiedad.numero) + ":" + str(self.precio)

    def get_absolute_url(self):
        return reverse("main:home")


# Agentes de la inmobiliaria, que realizan las acciones.
class Agente(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)

    # Esto define la representación del objeto.
    def __str__(self):
        return '%s %s' % (self.nombre, self.apellido)

    class Meta:
        verbose_name_plural = "agentes"


# Representa una visita de un Agente, con un Cliente a una Propiedad dada en una Fecha dada.
class Visita(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    agente = models.ForeignKey(Agente, default='1', on_delete=models.CASCADE)
    descripcion = models.TextField(max_length=100, default='')
    fecha = models.DateField(default=timezone.now)

    # propiedad.entrada = models.DateTimeField('date published')

    # Esto define la representación del objeto.
    def __str__(self):
        return (
                self.agente.nombre + " visito " + self.propiedad.direccion + str(
            self.propiedad.numero) + " con " + self.cliente.nombre + " " + self.cliente.apellido)

    def get_absolute_url(self):
        return reverse("main:home")


# Datos sobre las Operaciones inmobiliarias, Clientes comprador y vendedor, escribano, boleto, monto, Propiedad-
class Operacion(models.Model):
    nombre = models.CharField(max_length=500, default="operacionbien")
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    comprado_por = models.ForeignKey(Cliente, related_name='+', on_delete=models.CASCADE)
    vendido_por = models.ForeignKey(Cliente, related_name='+', on_delete=models.CASCADE)
    monto = models.PositiveIntegerField(default=0)
    fecha = models.DateTimeField(default=timezone.now)
    escribano = models.CharField(max_length=40, default="")
    boleto = models.BooleanField(blank=True)

    class Meta:
        verbose_name_plural = "operaciones"

    # propiedad.entrada = models.DateTimeField('date published')

    # Esto define la representación del objeto.
    def __str__(self):
        return "Se vendio" + self.propiedad.direccion + str(self.propiedad.numero)

    def get_absolute_url(self):
        return reverse("main:home")
