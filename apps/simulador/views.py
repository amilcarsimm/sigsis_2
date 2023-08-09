from django.shortcuts import render
from django.template import RequestContext, loader

from simulador.forms import *
from apps.modulo.models import Modulo, Roteiro

def simulador(request):
    
    modulos = Modulo.objects.order_by('mod_seq')
    roteiros = Roteiro.objects.order_by('rot_seq')
    
    simulador = get_simulador(request)
    template = loader.get_template('simulador-somente.html')
    context = RequestContext(request, {
        'modulos': modulos,
        'roteiros': roteiros,
        'simulador': simulador,
        }
    )
    
    return render(request, 'modulo/detalhe.html', context)
    #return HttpResponse(template.render(context))
