from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout, models
from .models import Ticket, Empleado
from django.db.models import Q
from .forms import TicketForm, KeywordForm, UserForm, TextDataForm, FileDataForm
from django.contrib.auth.models import User

DATA_FILE_TYPES = ['png', 'jpg', 'jpeg', 'xls', 'xlsx', 'word', 'wordx', 'pdf']


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'ticket/login.html')
    else:
        tickets = Ticket.objects.filter(cerrado=False)
        return render(request, 'ticket/' + request.user.empleado.perfil + '/index.html', {'tickets': tickets})


def detail(request, ticket_id):
    if not request.user.is_authenticated():
        return render(request, 'ticket/login.html')
    else:
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        user = request.user
        if str(request.user.empleado.perfil) == 'supervisor':
            operadores = User.objects.filter(empleado__perfil='operador')
            return render(request, 'ticket/' + request.user.empleado.perfil + '/detail.html',
                          {'ticket': ticket, 'operadores': operadores})
        else:
            return render(request, 'ticket/' + request.user.empleado.perfil + '/detail.html', {'ticket': ticket, 'user':user})


def mis_tickets(request):
    if not request.user.is_authenticated():
        return render(request, 'ticket/login.html')
    else:
        tickets = Ticket.objects.filter(cerrado=False, encargado=request.user)
        return render(request, 'ticket/' + request.user.empleado.perfil + '/index.html', {'tickets': tickets})


def tickets_no_asignados(request):
    if not request.user.is_authenticated():
        return render(request, 'ticket/login.html')
    else:
        if str(request.user.empleado.perfil) == 'supervisor':
            tickets = Ticket.objects.filter(asignado=False, cerrado=False)
            return render(request, 'ticket/' + request.user.empleado.perfil + '/index.html',
                          {'tickets': tickets})
        else:
            tickets = Ticket.objects.filter(cerrado=False)
            return render(request, 'ticket/' + request.user.empleado.perfil + '/index.html',
                          {'tickets': tickets})


def asignar_ticket(request):
    if not request.user.is_authenticated():
        return render(request, 'ticket/login.html')
    else:
        if str(request.user.empleado.perfil) == 'supervisor':
            user = User.objects.get(pk=request.POST['user'])
            ticket = Ticket.objects.get(pk=request.POST['ticket'])
            ticket.encargado = user
            ticket.asignado = True
            ticket.save()
            operadores = User.objects.filter(empleado__perfil='operador')
            return render(request, 'ticket/' + request.user.empleado.perfil + '/detail.html',
                          {'ticket': ticket, 'operadores': operadores})
        else:
            return redirect('ticket:index')



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
            return render(request, 'ticket/' + request.user.empleado.perfil + '/detail.html', {'ticket': ticket})
        perfil = request.user.empleado.perfil
        extiende = 'ticket/' + str(perfil) + '/base.html'
        context = {
            "form": form,
            "extiende": extiende,
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
                'error_message': 'Data file must be pdf, word, excel, jpg, jpeg png',
            }
            return render(request, 'ticket/' + request.user.empleado.perfil + '/create_data_file.html', context)

        data.save()
        return render(request, 'ticket/' + request.user.empleado.perfil + '/detail.html', {'ticket': ticket})
    context = {
        'ticket': ticket,
        'form': form,
    }
    return render(request, 'ticket/' + request.user.empleado.perfil + '/create_data_file.html', context)


def create_text_data(request, ticket_id):
    form = TextDataForm(request.POST or None)
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if form.is_valid():
        data = form.save(commit=False)
        data.ticket = ticket
        data.data_text = request.POST['data_text']
        data.save()
        return render(request, 'ticket/' + request.user.empleado.perfil + '/detail.html', {'ticket': ticket})
    context = {
        'ticket': ticket,
        'form': form,
    }
    return render(request, 'ticket/' + request.user.empleado.perfil + '/create_data_file.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                tickets = Ticket.objects.filter(creador=request.user)
                return render(request, 'ticket/' + request.user.empleado.perfil + '/index.html', {'tickets': tickets})
            else:
                return render(request, 'ticket/login.html', {'error_message': 'Tu cuenta ha sido desabilitada'})
        else:
            return render(request, 'ticket/login.html', {'error_message': 'Error en usuario o contraseña'})
    return render(request, 'ticket/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'ticket/login.html', context)


