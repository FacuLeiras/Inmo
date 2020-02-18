import pygal
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from .forms import ClienteMailForm, NuevaPropiedadForm, NuevoClienteForm, NuevoAgenteForm, NuevaVisitaForm, \
    NuevoMailForm, NuevoTelForm, NuevaOperacionForm, NuevoPrecioForm, NuevoDepartamentoForm, NuevaCasaForm
from main.models import Cliente, Propiedad, Telefono, Visita, Agente, Mail, Operacion, Propiedad_Precio, Casa, \
    Departamento
from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView
from .filters import FiltroCliente, FiltroPropiedad, FiltroVisita, FiltroOperacion, FiltroPrecio, FiltroCasa, FiltroDpto
import pandas as pd
from django.urls import reverse
from django.template import RequestContext
from bokeh.transform import cumsum

from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from math import pi


#Aqui se definen todas las vistar que interactuaran con la BD y seran renderizadas para el usuario


#
#
# Consultas, Graficos
# def Grafico(request):


# otro filtro? con click desde template puedo pero fijo. Dinamico con html tags?
def precioProp(request):
    model = Propiedad
    template_name = 'main/resultados_propiedad.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = FiltroPropiedad(self.request.GET, queryset=self.get_queryset())
        return context


def Pygal1(request):
    pie_chart = pygal.Pie()
    pie_chart.title = 'Browser usage in February 2012 (in %)'
    pie_chart.add('IE', 19.5)
    pie_chart.add('Firefox', 36.6)
    pie_chart.add('Chrome', 36.3)
    pie_chart.add('Safari', 4.5)
    pie_chart.add('Opera', 2.3)
    return pie_chart.render()


def Prueba(request, **kwargs):
    pk = kwargs.get("pk")
    x = []
    y = []
    prop = Propiedad.objects.get(id=pk)
    a = Propiedad_Precio.objects.filter(propiedad=prop).values().order_by('fecha')
    # print(pk)
    for i in a:
        x.append(i['fecha'])
        y.append(str(i['precio']))
    # print(x)
    # print(y)

    plot = figure(title="Valor de %s" % prop, x_axis_type="datetime", x_axis_label='Fecha', y_axis_label='Precio',
                  plot_width=400,
                  plot_height=400)
    plot.xaxis[0].formatter.days = "%d/%m/%Y"
    plot.xaxis.major_label_orientation = pi / 3
    plot.line(x, y, line_width=2)
    script, div = components(plot)
    # output_file("datetime.html")
    return render_to_response('main/graph2.html', {'script': script, 'div': div})


def Barra(request):
    p = figure(plot_width=400, plot_height=400, x_axis_label='Agentes',
               y_axis_label='Visitas')
    agentes = []
    for i in Agente.objects.all():
        agentes.append(i.nombre)
    print(agentes)
    visitas = []
    for i in agentes:
        visitas.append(Visita.objects.filter(agente__nombre=i).count())
    print(visitas)
    df = pd.DataFrame(columns=["agente", "visitas"])
    df['agente'] = agentes
    df['visitas'] = visitas
    print(df)
    hover = HoverTool(tooltips=[('Agente', '@agentes'),
                                ('Visita', '@visitas')])
    p.add_tools(hover)
    p = Barra(df, values='value', group='variable')
    # p.vbar(x=[1,2], width=0.5, bottom=0,
    #      top=visitas, color="firebrick")
    script, div = components(p)
    return render_to_response('main/graph2.html', {'script': script, 'div': div})

    # show(p)


def Pie(request):
    # data = pd.Series([0.15, 0.4, 0.7, 1.0], index=list('abcd')).reset_index(name='value').rename(columns={'index': 'agente'})
    a = Visita.objects.filter(agente='1').count()
    b = Visita.objects.filter(agente='2').count()
    print(a)
    print(b)
    x = {
        'Marilen': a,
        'Marcela': b
    }

    data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'agente'})
    data['angle'] = data['value'] / data['value'].sum() * 2 * pi
    # data['color'] = Blues8[len(x)]
    data['color'] = ['#084594', '#2171b5']
    p = figure(plot_height=350, title="Pie Chart", toolbar_location=None,
               tools="hover", tooltips="@agente: @value", x_range=(-0.5, 1.0))

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='Agentes', source=data)

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    script, div = components(p)
    # output_file("datetime.html")
    return render_to_response('main/graph2.html', {'script': script, 'div': div})
    # show(p)


def search(request):
    form = NuevoClienteForm()
    nom = request.GET("nombre")
    print(nom)
    return render_to_response('main/search.html', {'form': form})


def results(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        cli = Cliente.objects.filter(nombre=q.nombre)
        return render_to_response('main/results.html', {'clientes': cli})
    else:
        return HttpResponse('Please enter a valid input.')


def cantVisitasCliente(request, pk):
    visitas = Visita.objects.filter(cliente=pk)
    cant = Visita.objects.filter(cliente=pk).count()
    print(cant)


def cantVisitasProp(request, pk):
    visitas = Visita.objects.filter(propiedad=pk)
    cant = Visita.objects.filter(propiedad=pk).count()


def visitasDiaAg(request, **kwargs):
    date = kwargs.get("date")
    dia = Visita.objects.filter(fecha=date)

    pk = kwargs.get("pk")
    if (pk):
        agente = Agente.objects.get(pk=pk)
        diaAg = dia.filter(agente=agente)


def cambioPrecio(request, pk):
    cambios = Propiedad_Precio.objects.filter(propiedad=pk)
    cant = Propiedad_Precio.objects.filter(propiedad=pk).count()


# Create your views here.


#
#
# Pagina Principal
class HomePageView(TemplateView):
    template_name = 'main/home.html'


#
#
# Detalles de Modelos
class AgenteDetailView(DetailView):
    template_name = 'main/mostrar_agente.html'
    queryset = Agente.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Agente, pk=id_)


def detalleCliente(request, **kwargs):
    pk = kwargs.get("pk")
    cliente = Cliente.objects.get(pk=pk)
    mails = Mail.objects.filter(cliente=cliente.pk)
    telefonos = Telefono.objects.filter(cliente=cliente.pk)
    # print (mails)
    context = {
        'cliente': cliente,
        'mails': mails,
        'telefonos': telefonos,
    }
    return render(request, 'main/mostrar_cliente.html', context)


def detallePropiedad(request, **kwargs):
    pk = kwargs.get("pk")
    propiedad = Propiedad.objects.get(pk=pk)
    precio = Propiedad_Precio.objects.filter(propiedad=propiedad.pk).order_by('fecha').last()
    # print(precio)
    context = {
        'propiedad': propiedad,
        'precio': precio,
    }
    return render(request, 'main/mostrar_propiedad.html', context)


def detalleCasa(request, **kwargs):
    pk = kwargs.get("pk")
    propiedad = Casa.objects.get(pk=pk)
    precio = Propiedad_Precio.objects.filter(propiedad=propiedad.pk).order_by('fecha').last()
    # print(precio)
    context = {
        'casa': propiedad,
        'precio': precio,
    }
    return render(request, 'main/mostrar_casa.html', context)


def detalleDpto(request, **kwargs):
    pk = kwargs.get("pk")
    propiedad = Departamento.objects.get(pk=pk)
    precio = Propiedad_Precio.objects.filter(propiedad=propiedad.pk).order_by('fecha').last()
    # print(precio)
    context = {
        'departamento': propiedad,
        'precio': precio,
    }
    return render(request, 'main/mostrar_departamento.html', context)


class VisitaDetailView(DetailView):
    template_name = 'main/mostrar_visita.html'
    queryset = Visita.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Visita, pk=id_)


class OperacionDetailView(DetailView):
    template_name = 'main/mostrar_operacion.html'
    queryset = Operacion.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Operacion, pk=id_)


class PrecioDetailView(DetailView):
    template_name = 'main/mostrar_precio.html'
    queryset = Propiedad_Precio.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("pk")
        print(id_)
        return get_object_or_404(Propiedad_Precio, pk=id_)


#
#
# Altas
def altas(request):
    return render(request, 'main/altas.html', {})


def alta_cliente_mail(request):
    ClienteMailForm()
    if request.method == 'POST':
        form = ClienteMailForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            cliente = Cliente.objects.create(nombre=nombre, apellido=apellido)
            mail = form.cleaned_data['mail']
            Mail.objects.create(cliente=cliente, mail=mail)
            mail2 = form.cleaned_data['mail2']
            Mail.objects.create(cliente=cliente, mail=mail2)
            numero = form.cleaned_data['telefono']
            Telefono.objects.create(cliente=cliente, numero=numero)
            numero2 = form.cleaned_data['telefono2']
            if numero2: (
                Telefono.objects.create(cliente=cliente, numero=numero2)
            )

            return redirect('/')

    else:
        form = ClienteMailForm()
    return render(request, 'main/alta_cliente.html', {'form': form})


def alta_op(request):
    if request.method == 'POST':
        form = NuevaOperacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = NuevaOperacionForm()
    return render(request, 'main/alta_operacion.html', {'form': form})


def alta_prop(request):
    if request.method == 'POST':
        form = NuevaPropiedadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = NuevaPropiedadForm()
    return render(request, 'main/alta_prop.html', {'form': form})


class dptoCreateView(CreateView):
    model = Departamento
    form_class = NuevoDepartamentoForm
    template_name = "main/alta_departamento.html"


def alta_dpto(request):
    if request.method == 'POST':
        form = NuevoDepartamentoForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES)
            form.save()
            return redirect('/')
    else:
        form = NuevoDepartamentoForm()
    return render(request, 'main/alta_departamento.html', {'form': form})


def alta_casa(request):
    if request.method == 'POST':
        form = NuevaCasaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = NuevaCasaForm()
    return render(request, 'main/alta_casa.html', {'form': form})


def alta_agente(request):
    if request.method == 'POST':
        form = NuevoAgenteForm(request.POST)
        if form.is_valid():
            cli = form.save()
            return redirect('/')
    else:
        form = NuevoAgenteForm()
    return render(request, 'main/alta_agente.html', {'form': form})


def alta_visita(request):
    if request.method == 'POST':
        form = NuevaVisitaForm(request.POST)
        if form.is_valid():
            cli = form.save()
            return redirect('/')
    else:
        form = NuevaVisitaForm()
    return render(request, 'main/alta_visita.html', {'form': form})


def alta_mail(request):
    if request.method == 'POST':
        form = NuevoMailForm(request.POST)
        if form.is_valid():
            cli = form.save()

            return redirect('../alta_tel/')
            # return redirect('/')
    else:
        form = NuevoMailForm()
    return render(request, 'main/alta_mail.html', {'form': form})


def alta_tel(request):
    if request.method == 'POST':
        form = NuevoTelForm(request.POST)
        if form.is_valid():
            cli = form.save()
            return redirect('/')
    else:
        form = NuevoTelForm()
    return render(request, 'main/alta_mail.html', {'form': form})


def alta_precio(request):
    if request.method == 'POST':
        form = NuevoPrecioForm(request.POST)
        if form.is_valid():
            cli = form.save()
            return redirect('/')
    else:
        form = NuevoPrecioForm()
    return render(request, 'main/alta_precio.html', {'form': form})


#
#
# Updates
class ClienteUpdateView(UpdateView):
    template_name = 'main/alta_cliente.html'
    form_class = NuevoClienteForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Cliente, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class PropiedadUpdateView(UpdateView):
    template_name = 'main/alta_prop.html'
    form_class = NuevaPropiedadForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Propiedad, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class CasaUpdateView(UpdateView):
    template_name = 'main/alta_casa.html'
    form_class = NuevaCasaForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Casa, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class DptoUpdateView(UpdateView):
    template_name = 'main/alta_departamento.html'
    form_class = NuevoDepartamentoForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Departamento, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class VisitaUpdateView(UpdateView):
    template_name = 'main/alta_prop.html'
    form_class = NuevaVisitaForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Visita, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class OperacionUpdateView(UpdateView):
    template_name = 'main/alta_operacion.html'
    form_class = NuevaOperacionForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Operacion, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class PrecioUpdateView(UpdateView):
    template_name = 'main/alta_precio.html'
    form_class = NuevoPrecioForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Propiedad_Precio, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


#
#
# Busquedas, Filtros
def buscar(request):
    return render(request, 'main/buscar.html', {})


class BuscarClienteView(ListView):
    model = Cliente
    template_name = 'main/resultados_cliente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = FiltroCliente(self.request.GET, queryset=self.get_queryset())
        return context


class BuscarPrecioView(ListView):
    model = Propiedad_Precio
    template_name = 'main/resultados_precio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = FiltroPrecio(self.request.GET, queryset=self.get_queryset())
        return context


class BuscarPropiedad_Precio(ListView):
    model = Propiedad_Precio
    template_name = 'main/resultados_propiedad_precio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = FiltroPrecio(self.request.GET, queryset=self.get_queryset())


class BuscarPropiedadView(ListView):
    model = Propiedad
    template_name = 'main/buscar_propiedad.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = FiltroPropiedad(self.request.GET, queryset=self.get_queryset())
        # print (context['object_list'])
        return context


class BuscarCasaView(ListView):
    model = Casa
    template_name = 'main/resultados_casa.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = FiltroCasa(self.request.GET, queryset=self.get_queryset())
        # print (context['object_list'])
        return context


class BuscarDptoView(ListView):
    model = Departamento
    template_name = 'main/resultados_dpto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = FiltroDpto(self.request.GET, queryset=self.get_queryset())
        # print (context['object_list'])
        return context


class BuscarOperacionView(ListView):
    model = Operacion
    template_name = 'main/resultados_operacion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = FiltroOperacion(self.request.GET, queryset=self.get_queryset())
        return context


class BuscarVisitaView(ListView):
    model = Visita
    template_name = 'main/resultados_visita.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = FiltroVisita(self.request.GET, queryset=self.get_queryset())
        return context

    '''" def get_queryset(self): # new
        query = self.request.GET.get('q')
        ape = self.request.GET.get('r',None)
        object_list = Cliente.objects.filter(
            Q(nombre__icontains=query) | Q(apellido__icontains=ape)
        )
        return object_list'''


#
#
# Eliminar Datos
class ClienteDeleteView(DeleteView):
    template_name = 'main/delete_cliente.html'
    queryset = Cliente.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Cliente, id=id_)

    def get_success_url(self):
        return reverse('main:home')


# Elimina casas y departamentos (son propiedades)
class PropiedadDeleteView(DeleteView):
    template_name = 'main/delete_propiedad.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Propiedad, id=id_)

    def get_success_url(self):
        return reverse('main:home')


class VisitaDeleteView(DeleteView):
    template_name = 'main/delete_visita.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Visita, id=id_)

    def get_success_url(self):
        return reverse('main:home')


class OperacionDeleteView(DeleteView):
    template_name = 'main/delete_operacion.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Operacion, id=id_)

    def get_success_url(self):
        return reverse('main:home')


class PrecioDeleteView(DeleteView):
    template_name = 'main/delete_precio.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Propiedad_Precio, id=id_)

    def get_success_url(self):
        return reverse('main:home')
