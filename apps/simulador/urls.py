from django.urls import path
from apps.simulador.views import simulador
from apps.simulador import *

urlpatterns = [
        path('apps.simulador', simulador, name='simulador'),
]
