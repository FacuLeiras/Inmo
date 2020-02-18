from django.contrib import admin
from .models import Cliente, Propiedad, Visita, Telefono, Mail, Operacion, Agente,Propiedad_Precio, Departamento, Casa
# Register your models here.
# Estos modelos son los que apareceran en la pagina de Administrador

admin.site.register(Cliente)
admin.site.register(Propiedad)
admin.site.register(Visita)
admin.site.register(Telefono)
admin.site.register(Mail)
admin.site.register(Operacion)
admin.site.register(Agente)
admin.site.register(Propiedad_Precio)
admin.site.register(Departamento)
admin.site.register(Casa)