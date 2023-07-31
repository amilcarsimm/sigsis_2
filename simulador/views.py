from django.shortcuts import render
from django.http import HttpResponse
from simulador.forms import *

def index(request):
        return HttpResponse(render(request, 'simulador/index.html'))

def simulador(request):
        simulador = get_simulador(request)
        return render(request, 'simulador/simulador.html', {'simulador': simulador})

