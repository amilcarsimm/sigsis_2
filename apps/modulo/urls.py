from django.urls import path
#from django.urls import re_path as url
from apps.modulo.views import detalhe, index
from apps.simulador.views import simulador

# -*- coding: UTF-8 -*-
#from __future__ import unicode_literals


"""
sigsis URL Configuration
"""
from django.conf.urls import include
from django.contrib import admin
#from django.conf.urls.static import static
from django.conf import settings
#from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = [
    #para inclusão de link para recuperação de senha    
    #url(r'^admin/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
    #url(r'^admin/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    #url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    #url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    #path('admin/', admin.site.urls),
    #path('tinymce/', include('tinymce.urls')),
    #path('mce_filebrowser/', include('mce_filebrowser.urls')),
    #path(r'^tinymce/', include('tinymce.urls')),
    #path(r'^mce_filebrowser/', include('mce_filebrowser.urls')),
    #path(r'^static/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
    #path(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
    path('', index, name='index'),
    #path('index', index, name='index'),
    path('modulo/m(int:<mod_id>)/r(<int:rot_id>)', detalhe, name='roteiro'),
    path('simulador', simulador, name='simulador'),
]
