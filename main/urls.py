from django.conf.urls import url
from django.urls import path
from . import views
from django.views.generic import RedirectView
from .views import HomePageView, BuscarClienteView, BuscarPropiedadView, BuscarVisitaView, BuscarOperacionView, \
    ClienteUpdateView, PropiedadUpdateView, VisitaUpdateView, OperacionUpdateView, PrecioUpdateView, CasaUpdateView,\
    PrecioDetailView, BuscarPrecioView, ClienteDeleteView, PropiedadDeleteView, VisitaDeleteView, OperacionDeleteView, \
    PrecioDeleteView, BuscarPropiedad_Precio, detalleCasa, detalleDpto, BuscarCasaView, BuscarDptoView, DptoUpdateView, \
    dptoCreateView

app_name = "main"

urlpatterns = [

    # homePage
    path('', HomePageView.as_view(), name='home'),

    # path('graph/', views.bokeh, name='bokeh'),
    path('graph/<int:pk>/', views.Prueba, name='graficoPrecio'),
    path('pygal1/', views.Pygal1, name='graphPygal'),
    path('pie/', views.Pie, name='pie'),
    path('barra/', views.Barra, name='barra'),

    # detailViews
    path('cliente/<int:pk>/', views.detalleCliente, name='detalleCliente'),
    path('propiedad/<int:pk>/', views.detallePropiedad, name='detalle_propiedad'),
    path('visita/<int:pk>/', views.VisitaDetailView.as_view(), name='detalle_visita'),
    path('agente/<int:pk>/', views.AgenteDetailView.as_view(), name='detalle_agente'),
    path('operacion/<int:pk>/', views.OperacionDetailView.as_view(), name='detalle_operacion'),
    path('precio/<int:pk>/', views.PrecioDetailView.as_view(), name='detalle_precio'),
    path('casa/<int:pk>/', views.detalleCasa, name='detalle_casa'),
    path('dpto/<int:pk>/', views.detalleDpto, name='detalle_dpto'),


    # Updates
    path('cliente/<int:id>/update/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('propiedad/<int:id>/update/', PropiedadUpdateView.as_view(), name='propiedad_update'),
    path('visita/<int:id>/update/', VisitaUpdateView.as_view(), name='visita_update'),
    path('operacion/<int:id>/update/', OperacionUpdateView.as_view(), name='operacion_update'),
    path('precio/<int:id>/update/', PrecioUpdateView.as_view(), name='precio_update'),
    path('casa/<int:id>/update/', CasaUpdateView.as_view(), name='casa_update'),
    path('dpto/<int:id>/update/', DptoUpdateView.as_view(), name='dpto_update'),


    # altas
    path("alta_dpto/", dptoCreateView.as_view(), name="alta_dpto"),

    #path("alta_dpto/", views.alta_dpto, name="alta_dpto"),
    path("alta_casa/", views.alta_casa, name="alta_casa"),
    path("altas/", views.altas, name="altas"),
    path("alta_cliente/", views.alta_cliente_mail, name="alta_cliente_mail"),
    path("alta_agente/", views.alta_agente, name="alta_agente"),
    path("alta_mail/", views.alta_mail, name="alta_mail"),
    path("alta_tel/", views.alta_tel, name="alta_tel"),
    path("alta_prop/", views.alta_prop, name="alta_prop"),
    path("alta_visita/", views.alta_visita, name="alta_visita"),
    path("alta_op/", views.alta_op, name="alta_op"),
    path("alta_precio/", views.alta_precio, name="alta_precio"),

    # Busquedas
    path('buscar/', views.buscar, name='buscar'),
    path('buscar_cliente/', BuscarClienteView.as_view(), name='resultados_cliente'),
    path('buscar_visita/', BuscarVisitaView.as_view(), name='resultados_visita'),
    path('buscar_propiedad/', BuscarPropiedadView.as_view(), name='resultados_propiedad'),
    path('buscar_precio/', BuscarPrecioView.as_view(), name='resultados_precio'),
    path('buscar_casa/', BuscarCasaView.as_view(), name='resultados_casa'),
    path('buscar_dpto/', BuscarDptoView.as_view(), name='resultados_dpto'),

    # Busquedas de Jefa
    path('buscar_operacion/', BuscarOperacionView.as_view(), name='resultados_operacion'),
    path('buscar_precio/', BuscarPropiedad_Precio.as_view(), name='resultados_propiedad_precio'),



    # Eliminar
    path('eliminar_cliente/<int:id>/', ClienteDeleteView.as_view(), name='eliminar_cliente'),
    path('eliminar_propiedad/<int:id>/', PropiedadDeleteView.as_view(), name='eliminar_propiedad'),
    path('eliminar_visita/<int:id>/', VisitaDeleteView.as_view(), name='eliminar_visita'),
    path('eliminar_operacion/<int:id>/', OperacionDeleteView.as_view(), name='eliminar_operacion'),
    path('eliminar_precio/<int:id>/', PrecioDeleteView.as_view(), name='eliminar_precio'),


    # url(r'^$', views.home, name='home'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),

]
