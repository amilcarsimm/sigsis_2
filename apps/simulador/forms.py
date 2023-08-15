# -*- coding: UTF8 -*-
#from setup.settings import static
from django import forms

# Agg backend, which uses the C++ antigrain rendering engine to make nice PNGs. The Agg backend is also configured to recognize requests to generate other output formats (PDF, PS, EPS, SVG). The easiest way to configure Matplotlib to use Agg is to call:
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import pylab
from pylab import *
from scipy import signal, fftpack

from scipy.signal.waveforms import *
from numpy.core.multiarray import arange
from PIL import Image
from io import BytesIO

import random
import string
import time

from django.core.files.storage import FileSystemStorage
#===============================================================================
# from random import *
# random.seed() #inicia a semente dos número pseudo randômicos
# random_image_a = random.randrange(0, 100) # entre 0 e 100
# random_image_b = random.choice('abcdefghijklmnopqrstuvxyz') # seleciona um dos elementos aleatoriamente
#===============================================================================
graficos = FileSystemStorage(location='/setup/static/media/graficos')

# para evitar erros de renderização por gráficos com muitos dados
mpl.rcParams['agg.path.chunksize'] = 20000# conforme http://matplotlib.org/users/customizing.html

# uma lista de tuplas
S_NPF_CHOICES = [
    ('','---'),
    ('cos', 'cos'),
    ('sin', 'sen'),
    ('sinc', 'sinc'),
    ('sinc2', 'sinc²'),
    ('sawtooth', 'serra'),
    ('square', 'quadrada'),
    ('triangle', 'triangular'),
]

# para um complemento para o nome do arquivo do gráfico
def mk_str(size):

    chars = []
    #chars.extend([i for i in string.ascii_letters])
    chars.extend([i for i in string.digits])
    image_random = ''

    for i in range(0, size):
        image_random += chars[random.randint(0,9)]

        random.seed = int(time.time())#inicia a semente dos número pseudo randômicos
        random.shuffle(chars)

    return image_random

class SimuladorForms(forms.Form):
    # fieldset "Gráfico/Plano"
    titulo = forms.CharField(
        label='Título do gráfico',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'required': True,
                'class':'input_medio',
                'tabindex':1
            }
        )
    )
    #xrotulo = forms.CharField(label='Eixo das abcissas (X)', max_length=100, widget=forms.TextInput(attrs={'required': True, 'tabindex':2}))
    #yrotulo = forms.CharField(label='Eixo das ordenadas (Y)', max_length=100, widget=forms.TextInput(attrs={'required': True, 'tabindex':3}))
    t_start = forms.FloatField(
        label='Início do eixo [s]',
        widget=forms.NumberInput(
            attrs={
                'required': True,
                'class':'input_menor',
                'tabindex':4,
            }
        )
    )
    t_stop = forms.FloatField(
        label='Fim do eixo [s]',
        widget=forms.NumberInput(
            attrs={
                'required': True,
                'class':'input_menor',
                'tabindex':5
            }
        )
    )
    # fieldset "Sinal"
    dc = forms.FloatField(
        label='Componente de tensão contínua <i>DC</i> [V]',
        widget=forms.NumberInput(
            attrs={
                'required': True,
                'class':'input_menor',
                'tabindex':6
            }
        )
    )
    ampl = forms.FloatField(
        label='Amplitude <i>A</i> [V]',
        widget=forms.NumberInput(
            attrs={
                'required': True,
                'class':'input_menor',
                'tabindex':7
            }
        )
    )
    s_npf = forms.ChoiceField(
        label='Forma de Onda',
        choices=S_NPF_CHOICES,
        widget=forms.Select(
            attrs={
                'required': True,
                'class':'input_menor',
                'tabindex':8
            }
        )
    )
    freq = forms.FloatField(
        label='Frequência Fundamental <i>f</i> [Hz]',
        min_value= 1,
        widget=forms.NumberInput(
            attrs={
                'required': True,
                'class': 'input_menor',
                'tabindex': 9,
            }
        )
    )
    desl = forms.FloatField(
        label='Deslocamento no tempo [s]',
        widget=forms.NumberInput(
            attrs={
                'required': True,
                'class':'input_menor',
                'tabindex':10
            }
        )
    )
    # fieldset "Simulação"
    fs = forms.FloatField(
        label='Taxa de amostragem <i>f</i><sub>s</sub> [Hz]',
        widget=forms.NumberInput(
            attrs={
                'required': True,
                'class':'input_menor',
                'tabindex':11
            }
        )
    )
    quantiza = forms.IntegerField(
        label='N⁰ de Níveis de Quantização [2-256]',
        help_text='O valor deverá estar entre 2 e 256, pensando em potências de 2 (2¹ a 2⁸), teremos valores que variarão entre 1 bit a 8 bits.',
        min_value=2,
        max_value=256,
        widget=forms.NumberInput(
            attrs={
                'required': True,
                'class':'input_menor',
                'tabindex':12
            }
        )
    )
    niveis = forms.CharField(
        label='Níveis de Quantização',
        help_text='Para o Quantizador Genérico. Em ordem crescente e separados por espaço em branco.',
         max_length=100,
        widget=forms.TextInput(
            attrs={
                'required': True,
                'class':'input_medio',
                'strip': True,
                'tabindex':13
            }
        )
    )
    limiar_inf = forms.FloatField(
        label='Limiar inferior do nível [0-1]',
        help_text='Para o Quantizador Genérico. O número entre 0 e 1, refere-se a fração ou percentual para o limiar inferior do nível. Default: metade ou 0,5.',
        min_value=0.0,
        max_value=1.0,
        widget=forms.NumberInput(
            attrs={
                'required': True,
                'class':'input_menor',
                'step': '0.1',
                'tabindex':14
            }
        )
    )
    plot_sinal = forms.BooleanField(
        label='Sinal [Vermelho]',
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'tabindex':15
            }
        )
    )
    plot_fourier = forms.BooleanField(
        label='Transformada de Fourier [Azul]',
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'tabindex':16
            }
        )
    )
    plot_amostras = forms.BooleanField(
        label='Amostras [Verde - Tracejado]',
        required=False,
        widget=forms.CheckboxInput
        (attrs={
            'tabindex':17
            }
        )
    )
    plot_quant_g = forms.BooleanField(
        label='Sinal Quantizado - Genérico [Ciano]',
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'tabindex':18
            }
        )
    )
    plot_quant_mt = forms.BooleanField(
        label='Sinal Quantizado <i>Mid-tread</i> [Azul]',
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'tabindex':19
            }
        )
    )
    plot_quant_mr = forms.BooleanField(
        label='Sinal Quantizado <i>Mid-rise</i> [Magenta]',
        required=False,widget=forms.CheckboxInput(
            attrs={
                'tabindex':20
            }
        )
    )
    plot_quant_eq_mt = forms.BooleanField(
        label='Erro de Quantização <i>Mid-tread</i> [Cinza]',
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'tabindex':21
            }
        )
    )
    plot_quant_eq_mr = forms.BooleanField(
        label='Erro de Quantização <i>Mid-rise</i> [Preto]',
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'tabindex':22
            }
        )
    )
    plot_quant_eq_g = forms.BooleanField(
        label='Erro de Quantização Genérico [Cinza]',required=False,
        widget=forms.CheckboxInput(
            attrs={
                'tabindex':23
            }
        )
    )
    # imagem
    random_image = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

# definindo os valores iniciais
im = str(mk_str(8))# gerará um número com 8 dígitos para complementar o nome do gráfico
# dicionário
default_data = {
    'titulo': 'Gráfico',
    't_start': -0.5,
    't_stop': 0.5,
    'dc': 0,
    'ampl': 1,
    's_npf': 'cos',
    'freq': 5.0,
    'desl': 0,
    'fs': 40.0,
    'random_image': im,
    'quantiza':8,
    'niveis':'-0,95 -0,5 0,1 0,25 0,7',
    'limiar_inf':'0.5',
}# valores iniciais do simulador 'yrotulo': 'f(t) [V]', 'xrotulo': 't [s]'

def get_simulador(request):
    #  Processa o formulário do simulador
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SimuladorForms(request.POST)
        # check whether it's valid:
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            t_start = form.cleaned_data['t_start']
            t_stop = form.cleaned_data['t_stop']
            dc = form.cleaned_data['dc']
            ampl = form.cleaned_data['ampl']
            s_npf = form.cleaned_data['s_npf']
            freq = form.cleaned_data['freq']
            desl = form.cleaned_data['desl']
            fs = form.cleaned_data['fs']
            quantiza = form.cleaned_data['quantiza']
            niveis = form.cleaned_data['niveis']
            limiar_inf = form.cleaned_data['limiar_inf']
            plot_sinal = form.cleaned_data['plot_sinal']
            plot_fourier = form.cleaned_data['plot_fourier']
            plot_amostras = form.cleaned_data['plot_amostras']
            plot_quant_g = form.cleaned_data['plot_quant_g']
            plot_quant_mt = form.cleaned_data['plot_quant_mt']
            plot_quant_mr = form.cleaned_data['plot_quant_mr']
            plot_quant_eq_g = form.cleaned_data['plot_quant_eq_g']
            plot_quant_eq_mt = form.cleaned_data['plot_quant_eq_mt']
            plot_quant_eq_mr = form.cleaned_data['plot_quant_eq_mr']
            random_image = form.cleaned_data['random_image']

            # caso o início do gráfico seja maior que o fim
            if t_start >= t_stop:
                return SimuladorForms(request.POST, label_suffix=':')
            
            
            # caso a frequência seja <= 0
            # if freq <= 0:
            #     return SimuladorForms(request.POST, label_suffix=':')
            
            # caso a frequência seja <= 0
            # elif freq <= 0:
            #     msg = 'Simulação sem possibilidade\nde visualização.\nA frequência deve ser maior que zero.'
            #     return SimuladorForms(request.POST, label_suffix=':',)
            
            showimage(request, t_start, t_stop, dc, ampl, freq, desl, fs, s_npf, titulo, plot_sinal, plot_fourier, plot_amostras, plot_quant_g, plot_quant_mt, plot_quant_mr, plot_quant_eq_g, plot_quant_eq_mt, plot_quant_eq_mr, quantiza, niveis, limiar_inf, random_image)#xrotulo, yrotulo,

            return SimuladorForms(request.POST, label_suffix=':')

    # ao acessar a página pela 1a vez
    else:
        return SimuladorForms(default_data, label_suffix=':')


def constroi_onda_amostras(request, t_start, t_stop, dc, ampl, freq, desl, fs, s_npf):
    # Constrói o sinal e suas amostras

    # converte o recebido do simulador para float e cria os arange, para o sinal e para as amostras
    t_start_c = float(t_start)# forma para conversão para float
    t_stop_c = t_stop.__float__()# outra forma para conversão para float

    t_step = 1 / (100*float(freq))
    fs_c = float(fs)
    t = arange(t_start_c, t_stop_c, t_step)
    t2 = arange(t_start_c, t_stop_c, 1/fs_c)

    # verifica o tipo de onda e constrói o sinal e as amostras
    if str(s_npf)=='cos':
        s = float(dc) + float(ampl) * cos(2 * pi * float(freq) * (t + float(desl)))
        s2 = float(dc) + float(ampl) * cos(2 * pi * float(freq) * (t2 + float(desl)))
    elif str(s_npf)=='sin':
        s = float(dc) + float(ampl) * sin(2 * pi * float(freq) * (t + float(desl)))
        s2 = float(dc) + float(ampl) * sin(2 * pi * float(freq) * (t2 + float(desl)))
    elif str(s_npf)=='sinc':
        s = float(dc) + float(ampl) * sinc(2 * float(freq) * (t + float(desl)))
        s2 = float(dc) + float(ampl) * sinc(2 * float(freq) * (t2 + float(desl)))
    elif str(s_npf)=='sinc2':
        s = float(dc) + float(ampl) * sinc(float(freq) * (t + float(desl)))**2
        s2 = float(dc) + float(ampl) * sinc(float(freq) * (t2 + float(desl)))**2
    elif str(s_npf)=='sawtooth':
        s = float(dc) + float(ampl) * sawtooth(2 * pi * float(freq) * (t + float(desl)), width=1)
        s2 = float(dc) + float(ampl) * sawtooth(2 * pi * float(freq) * (t2 + float(desl)), width=1)
    elif str(s_npf)=='square':
        s = float(dc) + float(ampl) * signal.square(2 * pi * float(freq) * (t + float(desl)))
        s2 = float(dc) + float(ampl) * signal.square(2 * pi * float(freq) * (t2 + float(desl)))
    elif str(s_npf)=='triangle':
        # sawtooth por default vai de +1 para -1, por isso coloquei a ampl negativa para "corrigir" a onda
        s = float(dc) - float(ampl) * sawtooth(2 * pi * float(freq) * (t + float(desl)), width=0.5)
        s2 = float(dc) - float(ampl) * sawtooth(2 * pi * float(freq) * (t2 + float(desl)), width=0.5)

    return s, t, s2, t2

def verifica_niveis(request, dc, ampl, niveis):
    # verifica e trata o campo 'Níveis de Quantização para o Quantizador Genérico
    # retira espaços em branco do final e no inicio
    niveis = niveis.strip()
    # troca a vírgula por ponto
    niveis = niveis.replace(',','.')

    # verificaos caracteres
    if niveis.replace('-','').replace('.','').replace(' ','').isdigit() and (niveis.find('--')==-1) and (niveis.find('- ')==-1) and (niveis.find('..')==-1) and (niveis.find('. ')==-1):
        # separa os termos
        niveis = niveis.split(' ')
        # verifica cada um dos elementos - posicionamento do sinal negativo
        for e in niveis:
            if ((e.find('-') > 0) or (e.count('-')>1)):
                msg = 'Revise os dados\nno campo\n"Níveis de Quantização".\n\n Observe a posição\ndo sinal de negativo.'
                return msg, niveis

        # converte os termos para float
        niveis = [float(e) for e in niveis]
        # verifica ordenação crescente
        if sorted(niveis) == niveis:
            msg = ''
        else:
            msg = 'Revise os dados\nno campo\n"Níveis de Quantização".\n\nNúmeros não estão\n em ordem crescente.'
        return msg, niveis
    else:
        msg = 'Revise os dados\nno campo\n"Níveis de Quantização".\n\nProvável erro de posicionamento\ndo sinal negativo ou vírgula.\n\nPossibilidade de caracter\ndo tipo "letra".'
        return msg, niveis


def quantizacao_niveis(request, s, s2, dc, ampl, quantiza, niveis, limiar_inf, plot_quant):
    # Parâmetros para o quantizador: passo, níveis e limiares dos níveis
    # constrói vetor com os limiares de quantização

    # verifica o passo de quantização
    passo_quant = (amax(s) - amin(s))/quantiza #verifica a diferença entre o maior e o menor elemento de s e divide pelo n de níveis

    # popula os vetores com os limiares (50% do nível) dos níveis de quantização mid-tread e mid-rise
    if(plot_quant == 'mt'): vetor_niveis_lim = [k*passo_quant/2 + amin(s) for k in range(int(quantiza*2-1))]
    if(plot_quant == 'mr'): vetor_niveis_lim = [k*passo_quant/2 + amin(s) + passo_quant*0.5 for k in range(int(quantiza*2-1))]
    # popula os vetores com os limiares (lim_inf e lim_sup) dos níveis de quantização 'niveis'
    if(plot_quant == 'g'):
        niveis = verifica_niveis(request, dc, ampl, niveis)[1]
        vetor_niveis_lim = []
        for i in range(0,len(niveis)-1,1):
            lim = niveis[i] + (niveis[i+1] - niveis[i]) * limiar_inf
            vetor_niveis_lim.insert(i, niveis[i])
            vetor_niveis_lim.insert(i, lim)
        vetor_niveis_lim.insert(i, amax(niveis))
        vetor_niveis_lim.sort()

    return vetor_niveis_lim

def quantizacao_vetor(request, s, s2,  dc, ampl, quantiza, niveis, limiar_inf, plot_quant):

    s3 = [] # este será o vetor para as amostras quantizadas
    eq = [] # este será o vetor para os erros de quantização

    vetor_niveis_lim = quantizacao_niveis(request, s, s2, dc, ampl, quantiza, niveis, limiar_inf, plot_quant)

    # vetor da quantização e dos erros de quantização
    for i in range(0, len(s2), 1):
        for j in range(0, len(vetor_niveis_lim)-2,2):
            if s2[i] >= vetor_niveis_lim[j] and s2[i] < vetor_niveis_lim[j+1]:
                s3.insert(i, vetor_niveis_lim[j])
                # erro de quantização
                eq.insert(i, vetor_niveis_lim[j] - s2[i])
            if s2[i] >= vetor_niveis_lim[j+1] and s2[i] < vetor_niveis_lim[j+2]:
                s3.insert(i, vetor_niveis_lim[j+2])
                # erro de quantização
                eq.insert(i, vetor_niveis_lim[j+1] - s2[i])
        if s2[i] >= amax(vetor_niveis_lim):
            s3.insert(i, amax(vetor_niveis_lim))
            # erro de quantização
            eq.insert(i, amax(vetor_niveis_lim) - s2[i])
        if s2[i] < amin(vetor_niveis_lim):
            s3.insert(i, amin(vetor_niveis_lim))
            # erro de quantização
            eq.insert(i, amin(vetor_niveis_lim) - s2[i])

    return s3, eq

def titula_grafico(request, dc, ampl, freq, desl, fs, s_npf, titulo, plot_sinal, plot_fourier, plot_amostras, plot_quant_g, plot_quant_mt, plot_quant_mr, plot_quant_eq_g, plot_quant_eq_mt, plot_quant_eq_mr):
    # Constrói os títulos do gráfico
    if dc != 0: str_dc = str(dc) + '+'
    else: str_dc = ''

    if (ampl < 0 and ampl != -1): str_ampl = '(' + str(ampl) + ')'
    elif (ampl < 0 and ampl == -1): str_ampl = '-'
    elif (ampl > 0 and ampl != 1): str_ampl = str(ampl)
    else: str_ampl = ''

    if desl == 0: str_desl = 't'
    elif desl > 0: str_desl = '*(t + ' + str(desl) + ')'
    else: str_desl = '*(t ' + str(desl) + ')'

    # título do gráfico
    # tratando valores negativos e zerados de dc, amplitude e deslocamento, no título

    flag_subplot = subplot_image(request, plot_sinal, plot_fourier, plot_amostras, plot_quant_g, plot_quant_mt, plot_quant_mr, plot_quant_eq_g, plot_quant_eq_mt, plot_quant_eq_mr)

    if(flag_subplot == 3 and (s_npf!='sinc2' and s_npf!='sinc')):
        titulo = ('' + titulo + '\nFunção $f(t) = ' + str_dc + str_ampl + str(s_npf) + '(2\pi' + str(freq) + str_desl + ')$ e Transformada de Fourier')
    elif(flag_subplot == 3 and s_npf=='sinc'):
        titulo = ('' + titulo + '\nFunção $f(t) = ' + str_dc + str_ampl + str(s_npf) + '(2*' + str(freq) + str_desl + ')$ e Transformada de Fourier')
    elif(flag_subplot == 3 and s_npf=='sinc2'):
        titulo = ('' + titulo + '\nFunção $f(t) = ' + str_dc + str_ampl + 'sinc(' + str(freq) + str_desl + ')²$ e Transformada de Fourier')
    elif(flag_subplot == 2  and not (s_npf!='sinc2' or s_npf!='sinc')):
        titulo = ('' + titulo + '\nTransformada de Fourier da função $f(t) = ' + str_dc + str_ampl + str(s_npf) + '(2\pi' + str(freq) + str_desl + ')$')
    elif(flag_subplot == 2 and s_npf=='sinc'):
        titulo = ('' + titulo + '\nTransformada de Fourier da função $f(t) = ' + str_dc + str_ampl + str(s_npf) + '(2*' + str(freq) + str_desl + ')$')
    elif(flag_subplot == 2 and s_npf=='sinc2'):
        titulo = ('' + titulo + '\nTransformada de Fourier da função $f(t) = ' + str_dc + str_ampl + 'sinc(' + str(freq) + str_desl + ')²$')
    else:
        if(s_npf=='sinc'):titulo = ('' + titulo + '\n $f(t) = ' + str_dc + str_ampl + str(s_npf) + '(2*' + str(freq) + str_desl + ')$')
        elif(s_npf=='sinc2'):titulo = ('' + titulo + '\n $f(t) = ' + str_dc + str_ampl + 'sinc(' + str(freq) + str_desl + ')²$')
        else:titulo = ('' + titulo + '\n $f(t) = ' + str_dc + str_ampl + str(s_npf) + '(2\pi' + str(freq) + str_desl + ')$')
    return titulo

def subplot_image(request, plot_sinal, plot_fourier, plot_amostras, plot_quant_g, plot_quant_mt, plot_quant_mr, plot_quant_eq_g, plot_quant_eq_mt, plot_quant_eq_mr):
    # verifica a necessidade de subplot caso tenha fourier
    # flag para verificação da necessidade de subplot
    print(subplot_image)
    flag_subplot = 0
    if(plot_sinal or plot_amostras or plot_quant_g or plot_quant_mt or plot_quant_mr or plot_quant_eq_g or plot_quant_eq_mt or plot_quant_eq_mr):  flag_subplot += 1
    if(plot_fourier):  flag_subplot += 2
    return flag_subplot

def showimage(request, t_start, t_stop, dc, ampl, freq, desl, fs, s_npf, titulo, plot_sinal, plot_fourier, plot_amostras, plot_quant_g, plot_quant_mt, plot_quant_mr, plot_quant_eq_g, plot_quant_eq_mt, plot_quant_eq_mr, quantiza, niveis, limiar_inf, random_image):
    # Constrói a imagem do gráfico
    s = constroi_onda_amostras(request, t_start, t_stop, dc, ampl, freq, desl, fs, s_npf)[0]
    t = constroi_onda_amostras(request, t_start, t_stop, dc, ampl, freq, desl, fs, s_npf)[1]
    s2 = constroi_onda_amostras(request, t_start, t_stop, dc, ampl, freq, desl, fs, s_npf)[2]
    t2 = constroi_onda_amostras(request, t_start, t_stop, dc, ampl, freq, desl, fs, s_npf)[3]

    verifica_niveis(request, dc, ampl, niveis)
    flag_subplot = subplot_image(request, plot_sinal, plot_fourier, plot_amostras, plot_quant_g, plot_quant_mt, plot_quant_mr, plot_quant_eq_g, plot_quant_eq_mt, plot_quant_eq_mr)

    # para não embaralhar os rótulos do eixo x
    t2_x = t2
    if (len(t2)>30 and len(t2)<50):
        t2_x = []
        for i in arange(t2[0], t2[len(t2)-1], 2/fs):t2_x.append(i)
    elif (len(t2)>50):
        t2_x = []
        for i in arange(t2[0], t2[len(t2)-1], 4/fs):t2_x.append(i)
    else: t2_x = t2
    
    plots = []
    fig = plt.figure() # para adicionar o title a figura e não aos subplots ou plot
    # Para a imagem do gráfico
    # para que o gráfico tem uma margem em baixo e outra um pouco maior em cima para a legenda
    #ymin, ymax = ylim()   # return the current ylim
    #ylim(ymin - 0.01, ymax + 0.15)  # set the ylim to ymin, ymax

    # para plotar os múltiplos sinais
    # verifica arrays muito longos

    if len(s) > 12000 or len(t2) > 1000:
        msg = 'Simulação sem possibilidade\nde visualização.\nVerifique os parâmetros.'
        plt.text(0.5, 0.5, msg, ha="center", va="center", size=20, color='k', bbox=dict(boxstyle="circle, pad=0.5", fc="r", ec="y", lw=1, alpha=0.5)), tick_params(direction='out', length=6, labelbottom="off", labelleft="off")
    elif verifica_niveis(request, dc, ampl, niveis)[0]:
        msg = verifica_niveis(request, dc, ampl, niveis)[0]
        plt.text(0.5, 0.5, msg, ha="center", va="center", size=20, color='k', bbox=dict(boxstyle="circle, pad=0.5", fc="r", ec="y", lw=1, alpha=0.5)), tick_params(direction='out', length=6, labelbottom="off", labelleft="off")
    else:
        if (plot_fourier):
            plots.append('plot_fourier')
        if (plot_sinal):
            plots.append('plot_sinal')
        if(plot_amostras):
            plots.append('plot_amostras')
        if(plot_quant_g):
            plots.append('plot_quant_g')
        if(plot_quant_eq_g):
            plots.append('plot_quant_eq_g')
        if(plot_quant_mt):
            plots.append('plot_quant_mt')
        if(plot_quant_eq_mt):
            plots.append('plot_quant_eq_mt')
        if(plot_quant_mr):
            plots.append('plot_quant_mr')
        if(plot_quant_eq_mr):
            plots.append('plot_quant_eq_mr')
        
        if(len(plots) > 0):
            margem_legenda = 0.15
            if(len(plots) > 2 and len(plots) < 5): margem_legenda += 0.15
            elif(len(plots) > 4 and len(plots) < 7): margem_legenda += 0.15
            elif(len(plots) > 6 and len(plots) < 9): margem_legenda += 0.15
            
            for p in plots:
                if(p == 'plot_fourier'):
                    if (flag_subplot == 3): plt.subplot(212)
                    fa = 100*freq
                    nfft = 2**12
                    f = np.arange(-nfft/2, nfft/2) * (fa / nfft)
                    s5 = fftpack.fftshift(np.abs(fftpack.fft(s, n=nfft))) / fa
                    plot(f, s5, '-', linewidth=1.5, color='blue', label='Transformada de Fourier')
                    plt.ylabel('$F(f)$')
                    plt.xlabel('$f$ [Hz]$')
                    plt.xlim([-4*freq, 4*freq])
                    plt.legend(fancybox=True, loc='upper right', shadow=True, fontsize='small', ncol=2)
                    plt.grid(which='major', axis='both', color='k', linestyle=':')
                    # para que o gráfico tem uma margem em baixo e outra um pouco maior em cima para a legenda
                    ymin, ymax = ylim()   # return the current ylim
                    ylim(ymin - 0.01, ymax + 0.05)  # set the ylim to ymin, ymax
                elif(p != 'plot_fourier'):
                    if(flag_subplot == 3):
                        plt.subplot(211)
                    if(p == 'plot_sinal'):
                        plot(t, s, '-', linewidth=1.5, color='red', label='Sinal')
                    if(p == 'plot_amostras'):
                        plt.stem(t2, s2, linefmt='g--', markerfmt='go', label='Amostras', basefmt='k-')
                    if(p == 'plot_quant_g'):
                        sg = quantizacao_vetor(request, s, s2,  dc, ampl, quantiza, niveis, limiar_inf, 'g')[0]
                        plot(t2, sg, '-', linewidth=1.2, drawstyle='steps-post', color='cyan', label='Sinal Quantizado - Genérico')
                    if(p == 'plot_quant_eq_g'):
                        eq_g = quantizacao_vetor(request, s, s2,  dc, ampl, quantiza, niveis, limiar_inf, 'g')[1]
                        plot(t2, eq_g, ':', linewidth=1.5, drawstyle='steps-post', color='grey', label='Erro de Quantização - Genérico')
                    if(p == 'plot_quant_mt'):
                        s3 = quantizacao_vetor(request, s, s2,  dc, ampl, quantiza, niveis, limiar_inf, 'mt')[0]
                        plot(t2, s3, '-', linewidth=1.2, drawstyle='steps-post', color='blue', label='Sinal Quantizado - Mid-tread')
                    if(p == 'plot_quant_eq_mt'):
                        eq_mt = quantizacao_vetor(request, s, s2,  dc, ampl, quantiza, niveis, limiar_inf, 'mt')[1]
                        plot(t2, eq_mt, ':', linewidth=1.5, drawstyle='steps-post', color='grey', label='Erro de Quantização - Mid-tread')
                    if(p == 'plot_quant_mr'):
                        s4 = quantizacao_vetor(request, s, s2,  dc, ampl, quantiza, niveis, limiar_inf, 'mr')[0]
                        plot(t2, s4, linewidth=1.2, drawstyle='steps-post', color='magenta', label='Sinal Quantizado - Mid-rise')
                    if(p == 'plot_quant_eq_mr'):
                        eq_mr = quantizacao_vetor(request, s, s2,  dc, ampl, quantiza, niveis, limiar_inf,  'mr')[1]
                        plot(t2, eq_mr, ':', linewidth=1.5, drawstyle='steps-post', color='black', label='Erro de Quantização - Mid-rise')
        
                    plt.ylabel('$f(t)$ [V]')
                    plt.xlabel('$t$ [s]')
                    plt.xlim(min(t), max(t))
                    plt.xticks(t2_x, rotation=90, fontsize=8)
                    plt.legend(fancybox=True, loc='upper right', shadow=True, fontsize='small', ncol=2)
                    plt.grid(which='major', axis='both', color='k', linestyle=':')
                    # para que o gráfico tem uma margem em baixo e outra um pouco maior em cima para a legenda
                    ymin, ymax = ylim()   # return the current ylim
                    ylim(ymin - 0.01, ymax + margem_legenda)  # set the ylim to ymin, ymax
    
    # Para a imagem do gráfico
    # para que o gráfico tem uma margem em baixo e outra um pouco maior em cima para a legenda
    # ymin, ymax = ylim()   # return the current ylim
    # ylim(ymin - 0.01 * (ymax - ymin), ymax + 0.35 * (ymax - ymin))  # set the ylim to ymin, ymax
    
    if (flag_subplot == 0):
        msg = 'Nenhuma simulação\nfoi selecionada.'
        plt.text(0.5, 0.5, msg, ha="center", va="center", size=20, color='k', bbox=dict(boxstyle="circle, pad=0.5", fc="yellow", ec="y", lw=1, alpha=0.5)), tick_params(direction='out', length=6, labelbottom="off", labelleft="off")
    
    elif (flag_subplot == 1):
        # para não ocultar o xlabel
        fig.subplots_adjust(bottom=0.2)
    elif (flag_subplot == 3):
        fig.subplots_adjust(bottom=0.2)
        # para que um subplot não sobreponha o outro, espaço entre os subplots
        fig.subplots_adjust(hspace=0.4)
        # As stated in the previous section, the default parameters (in inches) for Matplotlib plots are 6.4 wide and 4.8 high.
        fig.set_figwidth(9) # para 2 subplots
        fig.set_figheight(8) # para 2 subplots

    # título
    fig.suptitle(titula_grafico(request, dc, ampl, freq, desl, fs, s_npf, titulo, plot_sinal, plot_fourier, plot_amostras, plot_quant_g, plot_quant_mt, plot_quant_mr, plot_quant_eq_g, plot_quant_eq_mt, plot_quant_eq_mr))

    im_buffer = BytesIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()

    pilImage = Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())

    pilImage.save(im_buffer, 'PNG')

    path_graph = 'setup/static/media/graficos/graph' + str(random_image) + '.png'
    print(path_graph)

    pylab.savefig(path_graph)
    pylab.close()

    return path_graph