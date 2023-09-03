"""
Django settings for setup project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import django
from django.utils.translation import gettext
django.utils.translation.ugettext = gettext
from pathlib import Path, os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'tinymce',
    # 'sorl.thumbnail',
    # 'mce_filebrowser',
    # 'widget_tweaks',# biblioteca para customizar elementos do form simulador no template
    'apps.modulo.apps.ModuloConfig',
    # 'apps.roteiro.apps.RoteiroConfig',
    'apps.simulador.apps.SimuladorConfig',
    # 'django_quill',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'setup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'setup/static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media

MEDIA_ROOT = os.path.join(BASE_DIR, 'setup/static/media')

MEDIA_URL = 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

'''
TINYMCE_JS_URL = os.path.join(STATIC_URL, 'django_tiny_mce/tiny_mce.js' )

TINYMCE_JS_ROOT = STATIC_ROOT + 'django_tinymce/'
#TINYMCE_FILEBROWSER = True # com isso não aparece a busca da inserção de imagem no admin

TINYMCE_SPELLCHECKER = True 
#TINYMCE_COMPRESSOR = True # com esse parâmetro não funciona

TINYMCE_DEFAULT_CONFIG = {
    'file_browser_callback': 'mce_filebrowser',
    'plugins' : "pagebreak, spellchecker, style, layer, table, lists, save, advhr, advimage, advlink, autolink, emotions, iespell, inlinepopups, insertdatetime, preview, media, searchreplace, print, contextmenu, paste, directionality, fullscreen, noneditable, visualchars, nonbreaking, xhtmlxtras, template, wordcount, advlist, autosave, media, visualblocks,",
    'theme': "advanced",    
    # Theme options
    'theme_advanced_buttons1' : "bold,italic,underline,strikethrough,sub,sup,|,removeformat,visualchars,|,justifyleft,justifycenter,justifyright,justifyfull,|,formatselect,fontselect,fontsizeselect,|,forecolor,backcolor,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,|,code,|,fullscreen,|",
    'theme_advanced_buttons2' : "tablecontrols,|,hr,|,charmap,image,media,insertfile,anchor,|,search,replace,|",

    'theme_advanced_toolbar_location' : "top",
    'theme_advanced_toolbar_align' : "left",
    'theme_advanced_statusbar_location' : "bottom",
    'theme_advanced_resizing' : 'true',
    'file_browser_callback': 'mce_filebrowser',
    'width': '100%',
    'height': '200',
    'cleanup_on_startup': True,
    'custom_uno_redo_levels': 10,
    'nowrap': False,
    #'relative_urls': False,
    #'paste_text_sticky': True,
    #'paste_text_sticky_default' : True,
    #'style_formats' : "[{title : 'Bold text', inline : 'strong'},{title : 'Red text', inline : 'span', styles : {color : '#ff0000'}},{title : 'Help', inline : 'strong', classes : 'help'},{title : 'Table styles'},{title : 'Table row 1', selector : 'tr', classes : 'tablerow'}]",
}
'''
#Sessao
SESSION_COOKIE_AGE = 43200 # 12 horas * 60 minutos * 60 segundos

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SESSION_SAVE_EVERY_REQUEST = True

# QUILL_CONFIGS = {
#     'default':{
#         'theme': 'snow',
#         'modules': {
#             'syntax': True,
#             'toolbar': [
#                 [
#                     {'font': []},
#                     {'header': []},
#                     {'align': []},
#                     'bold', 'italic', 'underline', 'strike', 'blockquote',
#                     {'color': []},
#                     {'background': []},
#                 ],
#                 ['code-block', 'link'],
#                 ['clean'],
#             ]
#         }
#     }
# }