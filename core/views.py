from django.shortcuts import render
from core.models import Evento

# Create your views here.


def lista_eventos(requests):
    usuario = requests.user
    evento = Evento.objects.all()
    dados = {'eventos':evento}
    return render(requests, 'agenda.html', dados)

