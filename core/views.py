from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


def login_user(requests):
    return render(requests, 'login.html')


def submit_login(requests):
    if requests.POST:
        username = requests.POST.get('username')
        password = requests.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(requests, usuario)
            return redirect('/')
        else:
            messages.error(requests, "Usuário ou senha inválido")
    return redirect('/')


def logout_user(requests):
    logout(requests)
    return redirect('/')


@login_required(login_url='/login/')
def lista_eventos(requests):
    usuario = requests.user
    evento = Evento.objects.filter(usuario=usuario)
    dados = {'eventos':evento}
    return render(requests, 'agenda.html', dados)

