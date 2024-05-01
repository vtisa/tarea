from django.shortcuts import get_object_or_404, render, redirect
from .models import RegistroEvento, Usuario, Evento
from .forms import EventoForm, RegistroEventoForm,UsuarioForm
from django.utils import timezone
from django.db.models import Count

def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('listar_evento')
    else:
        form = UsuarioForm()
    return render(request, 'crear_usuario.html', {'form': form})

def crear(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_evento')
    else:
        form = EventoForm()
    return render(request, 'crear.html', {'form': form})

def registrar(request):
    if request.method == 'POST':
        form = RegistroEventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_registros')
    else:
        form = RegistroEventoForm()
    return render(request, 'registrar.html', {'form': form})

def listar_evento(request):
    eventos = Evento.objects.all()
    return render(request, 'listar_evento.html', {'eventos': eventos})

def listar_registros(request):
    registros = RegistroEvento.objects.all()
    return render(request, 'listar_registros.html', {'registros': registros})

def eliminar_registro(request, pk):
    registro = get_object_or_404(RegistroEvento, pk=pk)
    if request.method == 'POST':
        registro.delete()
    return redirect('listar_registros')

def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    evento.delete()
    return redirect('listar_evento') 

def actualizar_registro(request, pk):
    registro = get_object_or_404(RegistroEvento, pk=pk)
    if request.method == 'POST':
        form = RegistroEventoForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            return redirect('listar_registros')
    else:
        form = RegistroEventoForm(instance=registro)
    return render(request, 'actualizar_registro.html', {'form': form})

def actualizar_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('listar_evento') 
    else:
        form = EventoForm(instance=evento)
    return render(request, 'actualizar_evento.html', {'form': form})

#consultas con ORM#

def contar_registros(request):
    evento_id = request.GET.get('evento_id')
    mensaje = None
    
    if evento_id:
        try:
            evento = Evento.objects.get(id=evento_id)
            registros = RegistroEvento.objects.filter(evento=evento).values('usuario').annotate(count=Count('usuario'))
            count = sum(r['count'] for r in registros)
            return render(request, 'contar_registros.html', {'count': count, 'evento': evento})
        except Evento.DoesNotExist:
            mensaje = 'El evento seleccionado no existe.'
    
    return render(request, 'contar_registros.html', {'mensaje': mensaje})
       

def contar_mes_actual(request):
    mes_actual = timezone.now().month
    count = Evento.objects.filter(
        fecha_inicio__month=mes_actual,
        fecha_fin__month=mes_actual
    ).count()
    return render(request, 'contar_mes_actual.html', {'count': count})



def usuarios_activos(request):
    usuarios_mas_activos = Usuario.objects.annotate(
        num_eventos=Count('registroevento')
    ).filter(num_eventos__gte=3).order_by('-num_eventos')
    
    usuarios_menos_activos = Usuario.objects.annotate(
        num_eventos=Count('registroevento')
    ).filter(num_eventos__range=(0, 2)).order_by('-num_eventos')
    
    return render(request, 'usuarios_activos.html', {'usuarios_mas_activos': usuarios_mas_activos, 'usuarios_menos_activos': usuarios_menos_activos})


def contar_eventos_organizados(request):
    usuario_email = request.GET.get('usuario_email')
    if usuario_email:
        count = Evento.objects.filter(organizador__email=usuario_email).count()
        return render(request, 'contar_eventos_organizados.html', {'count': count, 'usuario_email': usuario_email})
    else:
        return render(request, 'contar_eventos_organizados.html')