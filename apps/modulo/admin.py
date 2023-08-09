# -*- coding: UTF8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from models import Modulo, Roteiro, Index
from mce_filebrowser.admin import MCEFilebrowserAdmin

admin.site.site_header = "Tópicos de Conhecimento"
admin.site.index_title = "Administração do Site"
admin.site.site_title = "Tópicos de Conhecimento"
#admin.site.site_url = ""

class MCEFilebrowserAdmin(admin.ModelAdmin):
    #pass
    class Media:
        js = ('js/filebrowser_init.js',)
    
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('mod_nome', 'mod_seq')
    search_fields = ('mod_nome')    
    date_hierarchy = 'mod_data_ult_altera'

class RoteiroAdmin(MCEFilebrowserAdmin):
    list_display = ('rot_nome', 'rot_modulo', 'rot_seq')
    search_fields = ('rot_nome', 'rot_subsidio')
    list_filter = ('rot_modulo')
    date_hierarchy = 'rot_data_ult_altera'
    
    
class IndexAdmin(MCEFilebrowserAdmin):
    search_fields = ('index_titulo')
    list_filter = ('index_titulo')
    
# Register your models here.
admin.site.register(Modulo, ModuloAdmin)
admin.site.register(Roteiro, RoteiroAdmin)
admin.site.register(Index, IndexAdmin)


# Register your models here.
