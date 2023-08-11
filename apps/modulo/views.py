# -*- coding: UTF8 -*-
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404

from apps.modulo.models import Modulo, Roteiro, Index
from apps.simulador.forms import *



# Create your views here.
def index(request):
    modulos = Modulo.objects.order_by('mod_seq')
    roteiros = Roteiro.objects.order_by('rot_seq')
    indexs = Index.objects.order_by('index_titulo')
    
    '''
    template = loader.get_template('../templates/modulo/index.html')
    
    context = RequestContext(request, {
        'modulos': modulos,
        'roteiros': roteiros,
        'indexs': indexs,
        }
    )
    '''
    return render(request, 'modulo/index.html', {'modulos': modulos, 'roteiros': roteiros, 'indexs': indexs})
    #return HttpResponse(template.render(context))


def detalhe(request, mod_id, rot_id):
    
    modulos = Modulo.objects.order_by('mod_seq')
    roteiros = Roteiro.objects.order_by('rot_seq')
    
    modulo = get_object_or_404(Modulo, pk=mod_id)
    #modulo = Modulo.objects.get(id=mod_id)
    roteiro = get_object_or_404(Roteiro, pk=rot_id)
    #roteiro = Roteiro.objects.get(id=rot_id)

    simulador = get_simulador(request)

    '''
    template = loader.get_template('/templates/modulo/detalhe.html')
    
    context = RequestContext(request, {
        'modulo': modulo,
        'roteiro': roteiro,
        'modulos': modulos,
        'roteiros': roteiros,
        'simulador': simulador,
        }
    )
    '''
    return render(request, 'modulo/detalhe.html', {'modulo': modulo, 'roteiro': roteiro, 'modulos': modulos, 'roteiros': roteiros, 'simulador': simulador})
    #return HttpResponse(template.render(context))
    
