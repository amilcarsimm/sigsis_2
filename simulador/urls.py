from django.urls import path
from simulador.views import index, simulador
from simulador import *

urlpatterns = [
        path('', index, name='index'),
        path('simulador/', simulador, name='simulador'),
]