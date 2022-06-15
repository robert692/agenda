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


@login_required(login_url='/login/')
def evento(requests):
    id_evento = requests.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(requests, 'evento.html', dados)


@login_required(login_url='/login/')
def submit_evento(requests):
    if requests.POST:
        titulo = requests.POST.get('titulo')
        data_evento = requests.POST.get('data_evento')
        descricao = requests.POST.get('descricao')
        local_evento = requests.POST.get('local_evento')
        usuario = requests.user
        id_evento = requests.POST.get('id_evento')
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.data_evento = data_evento
                evento.descricao = descricao
                evento.local_evento = local_evento
                evento.save()
            # Evento.objects.filter(id=id_evento).update(titulo=titulo,
            #                                            data_evento=data_evento,
            #                                            descricao=descricao,
            #                                            local_evento=local_evento)
        else:
            Evento.objects.create(titulo=titulo,
                                  data_evento=data_evento,
                                  descricao=descricao,
                                  local_evento=local_evento,
                                  usuario=usuario)
    return redirect('/')


@login_required(login_url='/login/')
def delete_evento(requests, id_evento):
    usuario = requests.user
    evento = Evento.objects.get(id=id_evento)
    if usuario == evento.usuario:
        evento.delete()
    return redirect('/')
