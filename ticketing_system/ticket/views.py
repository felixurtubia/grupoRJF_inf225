# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Ticket, TextData, FileData, Notificacion
from django.db.models import Q
from .forms import TicketForm, KeywordForm, UserForm, TextDataForm, FileDataForm, VinculoForm, AplazarForm
from django.contrib.auth.models import User
from datetime import datetime, date, timedelta
from django.core.urlresolvers import reverse, reverse_lazy

# tipo de archivo permitido para cargar la data

DATA_FILE_TYPES = ['png', 'jpg', 'jpeg', 'xls', 'xlsx', 'word', 'wordx', 'pdf']

# Funcion para crear notificaciones a usuarios
def enviarNotificacion(grupo_destino, usuario_origen, texto, tipo, ticket):
    for usuario in grupo_destino:
        Notificacion.objects.create(usuario_origen=usuario_origen, usuario_destino=usuario,
                                    texto=texto, tipo=tipo, ticket=ticket)


def consultarNotificaciones(user):
    if hasattr(user, 'notificaciones'):
        min_td = datetime.now() - timedelta(minutes=10)
        notificaciones = user.notificaciones.filter(fecha__gte=min_td)
        return notificaciones
    else:
        return []

# pagina principal de cada usuario logeado
def index(request):
    context = {'tickets_active': 'active', 'mis_tickets_active': '', 'tickets_cerrados_active': '',
               'tickets_eliminados_active': '', 'tickets_no_asignados_active': '', 'tickets_aplazados_active': '',
               'notificaciones': consultarNotificaciones(request.user)}
    if not request.user.is_authenticated():
        return render(request, 'ticket/login.html')
    else:
        context['tickets'] = Ticket.objects.filter(cerrado=False, eliminado=False, aplazado=False)
        context['base'] = 'ticket/' + request.user.empleado.perfil + '/base.html'
        return render(request, 'ticket/index.html', context)


# se aplican filtros para la lista de los tickets y se envia a index
def vista(request, tag=''):
    if not request.user.is_authenticated():
        return render(request, 'ticket/login.html')
    else:

        context = dict(tickets_active='', mis_tickets_active='', tickets_cerrados_active='',
                       tickets_eliminados_active='', tickets_no_asignados_active='', tickets_aplazados_active='')
        context['base'] = 'ticket/' + request.user.empleado.perfil + '/base.html'
        context['notificaciones'] = consultarNotificaciones(request.user)
        if tag == 'mis_tickets':
            context['tickets'] = Ticket.objects.filter(cerrado=False, eliminado=False, aplazado=False,
                                                       encargado=request.user)
            context['mis_tickets_active'] = 'active'
        elif tag == 'cerrados':
            context['tickets'] = Ticket.objects.filter(cerrado=True, eliminado=False, aplazado=False)
            context['tickets_cerrados_active'] = 'active'
        elif tag == 'eliminados':
            context['tickets'] = Ticket.objects.filter(eliminado=True, aplazado=False)
            context['tickets_eliminados_active'] = 'active'
        elif tag == 'no_asignados':
            context['tickets'] = Ticket.objects.filter(cerrado=False, eliminado=False, asignado=False, aplazado=False)
            context['tickets_no_asignados_active'] = 'active'
        elif tag == 'aplazados':
            context['tickets'] = Ticket.objects.filter(cerrado=False, eliminado=False, aplazado=True)
            context['tickets_aplazados_active'] = 'active'
            context['tiempo_aplazo_display'] = True
        else:
            context['tickets'] = Ticket.objects.filter(cerrado=False, eliminado=False, aplazado=False)
        return render(request, 'ticket/index.html', context)


# detalle de un ticket, recibe el usuario y el id del ticket
def detail(request, ticket_id):
    if not request.user.is_authenticated():
        return render(request, 'ticket/login.html')
    else:
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        user = request.user
        if str(request.user.empleado.perfil) == 'supervisor' or str(request.user.empleado.perfil) == 'jefe':
            operadores = User.objects.filter(empleado__perfil='operador')
            return render(request, 'ticket/' + request.user.empleado.perfil + '/detail.html',
                          {'ticket': ticket, 'operadores': operadores, 'permisos': 'supervisor',
                           'notificaciones': consultarNotificaciones(request.user)})
        else:
            return render(request, 'ticket/' + request.user.empleado.perfil + '/detail.html',
                          {'ticket': ticket, 'user': user, 'notificaciones': consultarNotificaciones(request.user)})


# Click de notificacion
def click_notificacion(request, notificacion_id):
    if not request.user.is_authenticated():
        return render(request, 'ticket/login.html')
    else:
        notificacion = get_object_or_404(Notificacion, pk=notificacion_id)
        if notificacion.ticket is not None:
            ticket_id = notificacion.ticket.id
            notificacion.delete()
            return redirect('ticket:detail', ticket_id)
        else:
            notificacion.delete()
            return redirect('ticket:index')


# se aplica una accion sobre un TICKET, solo puede ser hecho por supervisor (agregar al jefe)
def accion(request, ticket_id, accion):
    if not request.user.is_authenticated():
        return render(request, 'ticket/login.html')
    else:
        if not (str(request.user.empleado.perfil) == 'supervisor' or str(request.user.empleado.perfil) == 'jefe'):
            return redirect('ticket:index')
        else:
            if accion == 'asignar':
                user = User.objects.get(pk=request.POST['user'])
                ticket = Ticket.objects.get(pk=request.POST['ticket'])
                # Se asigna ticket
                ticket.encargado = user
                ticket.asignado = True
                ticket.save()
                # Se crea notificacion a encargado
                enviarNotificacion([user], request.user, 'Se te ha encargado el Ticket: "'+ticket.titulo+'"', 'TAsignado', ticket)
                return redirect('ticket:detail', ticket_id)
            elif accion == 'cerrar':
                ticket = get_object_or_404(Ticket, pk=ticket_id)
                ticket.cerrador = request.user
                ticket.cerrado = True
                ticket.save()
                # Se crea notificacion a todos menos administradores
                personas = User.objects.exclude(empleado__perfil='administrador')
                enviarNotificacion(personas, request.user, 'Ticket cerrado: "'+ticket.titulo+'"', 'TCerrado', ticket)
                return redirect('ticket:detail', ticket_id)
            elif accion == 'abrir':
                ticket = get_object_or_404(Ticket, pk=ticket_id)
                ticket.cerrador = None
                ticket.cerrado = False
                ticket.save()
                # Se crea notificacion a todos menos administradores
                personas = User.objects.exclude(empleado__perfil='administrador')
                enviarNotificacion(personas, request.user, 'Ticket abierto: "'+ticket.titulo+'"', 'Tabierto', ticket)
                return redirect('ticket:detail', ticket_id)
            elif accion == 'eliminar':
                ticket = get_object_or_404(Ticket, pk=ticket_id)
                ticket.eliminador = request.user
                ticket.eliminado = True
                ticket.save()
                # Se crea notificacion a todos menos administradores
                personas = User.objects.exclude(empleado__perfil='administrador')
                enviarNotificacion(personas, request.user, 'Ticket eliminado: "'+ticket.titulo+'"', 'TEliminado', ticket)
                return redirect('ticket:detail', ticket_id)
            elif accion == 'restaurar':
                ticket = get_object_or_404(Ticket, pk=ticket_id)
                ticket.eliminador = None
                ticket.eliminado = False
                ticket.save()
                # Se crea notificacion a todos menos administradores
                personas = User.objects.exclude(empleado__perfil='administrador')
                enviarNotificacion(personas, request.user, 'Ticket restaurado: "'+ticket.titulo+'"', 'Trestaurado', ticket)
                return redirect('ticket:detail', ticket_id)
            elif accion == 'editar':
                ticket = get_object_or_404(Ticket, pk=ticket_id)
                form = TicketForm(request.POST or None, instance=ticket)
                if form.is_valid():
                    ticket = form.save(commit=False)
                    ticket.asunto = request.POST['asunto']
                    ticket.contenido = request.POST['contenido']
                    ticket.save()
                    # Se crea notificacion a el operador encargado
                    enviarNotificacion([ticket.encargado], request.user,
                                       'Ticket editado: "'+ticket.titulo+'"', "TEditado", ticket)
                    return redirect('ticket:detail', ticket_id)
                context = {
                    'ticket': ticket,
                    'form': form,
                    'base': 'ticket/' + request.user.empleado.perfil + '/base.html',
                    'notificaciones': consultarNotificaciones(request.user)
                }
                return render(request, 'ticket/editar.html', context)

            elif accion == 'vincular':
                form = VinculoForm(request.POST or None)
                ticket = get_object_or_404(Ticket, pk=ticket_id)
                if form.is_valid():
                    if form.cleaned_data["ticket_padre"] == ticket:
                        form = VinculoForm(request.POST or None)
                        context = {
                            'ticket': ticket,
                            'form': form,
                            'base': 'ticket/' + request.user.empleado.perfil + '/base.html',
                            'error_message': "El ticket no puede ser vinculado a si mismo",
                            'notificaciones': consultarNotificaciones(request.user)
                        }
                        return render(request, 'ticket/create_vinculo.html', context)

                    vinculo = form.save(commit=False)
                    vinculo.ticket_hijo = ticket
                    vinculo.save()
                    # Se crea notificacion a el operador encargado
                    enviarNotificacion([ticket.encargado], request.user, 'Ticket Vinculado: "'+ticket.titulo+'"', "TVinculado",
                                       ticket)
                    return redirect('ticket:detail', ticket_id)
                context = {
                    'ticket': ticket,
                    'form': form,
                    'base': 'ticket/' + request.user.empleado.perfil + '/base.html',
                    'notificaciones': consultarNotificaciones(request.user)
                }
                return render(request, 'ticket/create_vinculo.html', context)
            elif accion == 'aplazar':
                form = AplazarForm(request.POST or None)
                ticket = get_object_or_404(Ticket, pk=ticket_id)
                if form.is_valid():
                    fecha = form.cleaned_data['fecha_aplazo']
                    ticket.fecha_aplazo = fecha
                    ticket.tiempo_restante_aplazo = fecha - date.today()
                    ticket.aplazado = True
                    ticket.save()
                    # Se crea notificacion a todos menos administradores
                    personas = User.objects.exclude(empleado__perfil='administrador')
                    enviarNotificacion(personas, request.user, 'Ticket aplazado: "'+ticket.titulo+'"', 'TAplazado', ticket)
                    return redirect('ticket:detail', ticket_id)
                context = {
                    'ticket': ticket,
                    'form': form,
                    'base': 'ticket/' + request.user.empleado.perfil + '/base.html',
                    'notificaciones': consultarNotificaciones(request.user)
                }
                return render(request, 'ticket/create_aplazar.html', context)
            else:
                redirect('ticket:index')


# visar o no visar para cada una de las leseeeras
def visar_text(request, data_id, ticket_id):
    if not request.user.is_authenticated():
        return render(request, 'ticket/login.html')
    else:
        data = get_object_or_404(TextData, pk=data_id)
        if str(request.user.empleado.perfil) == 'supervisor' or data.ticket.encargado == request.user:
            ticket = get_object_or_404(Ticket, pk=ticket_id)
            data.visada = True
            data.save()
            operadores = User.objects.filter(empleado__perfil='operador')
            return render(request, 'ticket/' + request.user.empleado.perfil + '/detail.html',
                          {'ticket': ticket, 'operadores': operadores, 'user': request.user,
                           'notificaciones': consultarNotificaciones(request.user)})
        else:
            return redirect('ticket:index')


def no_visar_text(request, data_id, ticket_id):
    if not request.user.is_authenticated():
        return render(request, 'ticket/login.html')
    else:
        data = get_object_or_404(TextData, pk=data_id)
        if str(request.user.empleado.perfil) == 'supervisor' or data.ticket.encargado == request.user:
            ticket = get_object_or_404(Ticket, pk=ticket_id)
            data.visada = False
            data.save()
            operadores = User.objects.filter(empleado__perfil='operador')
            return render(request, 'ticket/' + request.user.empleado.perfil + '/detail.html',
                          {'ticket': ticket, 'operadores': operadores, 'user': request.user,
                           'notificaciones': consultarNotificaciones(request.user)})
        else:
            return redirect('ticket:index')


def visar_file(request, data_id, ticket_id):
    if not request.user.is_authenticated():
        return render(request, 'ticket/login.html')
    else:
        data = get_object_or_404(FileData, pk=data_id)
        if str(request.user.empleado.perfil) == 'supervisor' or data.ticket.encargado == request.user:
            ticket = get_object_or_404(Ticket, pk=ticket_id)
            data.visada = True
            data.save()
            operadores = User.objects.filter(empleado__perfil='operador')
            return render(request, 'ticket/' + request.user.empleado.perfil + '/detail.html',
                          {'ticket': ticket, 'operadores': operadores, 'user': request.user,
                           'notificaciones': consultarNotificaciones(request.user)})
        else:
            return redirect('ticket:index')


def no_visar_file(request, data_id, ticket_id):
    if not request.user.is_authenticated():
        return render(request, 'ticket/login.html')
    else:
        data = get_object_or_404(FileData, pk=data_id)
        if str(request.user.empleado.perfil) == 'supervisor' or data.ticket.encargado == request.user:
            ticket = get_object_or_404(Ticket, pk=ticket_id)
            data.visada = False
            data.save()
            operadores = User.objects.filter(empleado__perfil='operador')
            return render(request, 'ticket/' + request.user.empleado.perfil + '/detail.html',
                          {'ticket': ticket, 'operadores': operadores, 'user': request.user,
                           'notificaciones': consultarNotificaciones(request.user)})
        else:
            return redirect('ticket:index')


# crear un ticket, crea una forma y la muestra en un template
def create_ticket(request):
    if not request.user.is_authenticated():
        return render(request, 'ticket/login.html')
    else:
        form = TicketForm(request.POST or None)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.creador = request.user
            ticket.asunto = request.POST['asunto']
            ticket.contenido = request.POST['contenido']
            ticket.save()
            personas = User.objects.exclude(empleado__perfil='administrador')
            enviarNotificacion(personas, request.user, 'Ticket creado: "'+ticket.titulo+'" ', 'TCreado', ticket)
            return redirect('ticket:detail', ticket.id)
        perfil = request.user.empleado.perfil
        extiende = 'ticket/' + str(perfil) + '/base.html'
        context = {
            "form": form,
            "extiende": extiende,
            'notificaciones': consultarNotificaciones(request.user)
        }
        return render(request, 'ticket/create_ticket.html', context)


def create_file_data(request, ticket_id):
    form = FileDataForm(request.POST or None, request.FILES or None)
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if form.is_valid():
        data = form.save(commit=False)
        data.ticket = ticket
        data.data_file = request.FILES['data_file']
        file_type = data.data_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in DATA_FILE_TYPES:
            context = {
                'ticket': ticket,
                'form': form,
                'error_message': 'Tipo de archivo debe ser pdf, word, excel, jpg, jpeg, png',
                'base': 'ticket/' + request.user.empleado.perfil + '/base.html',
                'notificaciones': consultarNotificaciones(request.user)
            }
            return render(request, 'ticket/create_data_file.html', context)

        data.save()
        return render(request, 'ticket/' + request.user.empleado.perfil + '/detail.html',
                      {'ticket': ticket, 'user': request.user, 'notificaciones': consultarNotificaciones(request.user)})
    context = {
        'ticket': ticket,
        'form': form,
        'base': 'ticket/' + request.user.empleado.perfil + '/base.html',
        'notificaciones': consultarNotificaciones(request.user)
    }
    return render(request, 'ticket/create_data_file.html', context)


def create_text_data(request, ticket_id):
    form = TextDataForm(request.POST or None)
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if form.is_valid():
        data = form.save(commit=False)
        data.ticket = ticket
        data.data_text = request.POST['data_text']
        data.save()
        return redirect('ticket:detail', ticket_id)
    context = {
        'ticket': ticket,
        'form': form,
        'base': 'ticket/' + request.user.empleado.perfil + '/base.html'
    }
    return render(request, 'ticket/create_data_file.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                tickets = Ticket.objects.filter(eliminado=False, cerrado=False, aplazado=False)
                return render(request, 'ticket/index.html',
                              {'tickets': tickets, 'base': 'ticket/' + request.user.empleado.perfil + '/base.html',
                               'notificaciones': consultarNotificaciones(request.user)})
            else:
                return render(request, 'ticket/login.html', {'error_message': 'Tu cuenta ha sido deshabilitada.'})
        else:
            return render(request, 'ticket/login.html', {'error_message': 'Error en usuario o contraseña.'})
    return render(request, 'ticket/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'ticket/login.html', context)
