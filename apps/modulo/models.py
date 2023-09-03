# -*- coding: UTF8 -*-
#from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# from django_quill.fields import QuillField

# class QuillPost(models.Model):
#     content = QuillField()

class Modulo(models.Model):
    mod_nome = models.CharField(max_length=100, verbose_name='Título do Módulo', unique=True)
    mod_seq = models.IntegerField(default=0, verbose_name='Número de sequência do Módulo', unique=True)
    mod_objetivo_geral = models.CharField(max_length=500, verbose_name='Objetivo Geral do Módulo')
    mod_data_criado = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    mod_data_ult_altera = models.DateTimeField(auto_now=True, verbose_name='Data da Última Alteração')

    class Meta:
        ordering = ['mod_seq']
        verbose_name = 'Módulo'
        
    def __str__(self):
        return self.mod_nome
    
    
class Roteiro(models.Model):
    ROT_SIM = (
        ('0', 'Sem Simulador'),
        ('1', 'Sinal'),
        ('2', 'Amostras'),
        ('3', 'Quantizador Genérico'),
        ('4', 'Quantizador Uniforme')
    )

    rot_nome = models.CharField(max_length=100, verbose_name='Título do Roteiro', unique=True)
    rot_seq = models.IntegerField(verbose_name='Número de sequência do Roteiro')
    rot_objetivo_geral = models.CharField(max_length=500, verbose_name='Objetivo Geral do Roteiro')
    rot_objetivos_espec = models.TextField(verbose_name='Objetivos Específicos do Roteiro')
    rot_modulo = models.ForeignKey(Modulo, verbose_name='Módulo', on_delete=models.CASCADE)
    rot_simulador = models.CharField(default='1', max_length=1, verbose_name='Simulador do Roteiro', choices=ROT_SIM)
    rot_subsidio = models.TextField(verbose_name='Subsídios do Roteiro')
    rot_biblio = models.TextField(verbose_name='Bibliografia do Roteiro')
    rot_exercicios = models.TextField(verbose_name='Exercícios do Roteiro')
    rot_data_criado = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    rot_data_ult_altera = models.DateTimeField(auto_now=True, verbose_name='Data da Última Alteração')

    class Meta:
        unique_together = ('rot_modulo', 'rot_seq')
        ordering = ['rot_modulo','rot_seq',]
        verbose_name = 'Roteiro'
        
    def __str__(self):
        return self.rot_nome

class Index(models.Model):
    index_titulo = models.CharField(max_length=100, verbose_name='Título do Texto')
    index_text = models.TextField(verbose_name='Texto da página Home/Index')
    index_data_criado = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    index_data_ult_altera = models.DateTimeField(auto_now=True, verbose_name='Data da Última Alteração')

    class Meta:
        ordering = ['index_titulo', 'index_data_criado','index_data_ult_altera',]
        verbose_name = 'Index'
        
    def __str__(self):
        return self.index_titulo
