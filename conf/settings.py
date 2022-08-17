"""
Django settings for conf project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from os import environ as env
from pathlib import Path
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', False)

ALLOWED_HOSTS = env.get('DJANGO_ALLOWED_HOSTS').split(' ')

# administradores y encargados del sistema
ADMINS = (('Webmaster', str(env.get('WEBMASTER_EMAIL'))), ('Administrador', env.get('ADMINISTRADOR_EMAIL')))
MANAGERS = ADMINS

# Envío de mensajes internos
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'debug_toolbar',
    
    'core.agenda', # permite la comunicación entre apoderados y profesores, inspectores o administrativos
    'core.dash', # app base privada
    'core.usuarios', # app para el control de los usuarios, roles y permisos
    'core.asistencia', # app para el control de la asistencia de los usuarios
    'core.cursos', # app para la creación de cursos y asignación de alumnos a cada curso
    'core.asignaturas', # app para la creación de asignaturas y asignación de estas a cada curso
    'core.calendario', # app para ver el horario de clases del alumno
    'core.libro_clases', # app para la digitalización del libro de clases
    'core.public', # app base pública
    'core.mensualidades', # app para el control de las mensualidades
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'querycount.middleware.QueryCountMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'conf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    STATIC_ROOT = [
        '/usr/src/app/static',
    ]
    MEDIA_ROOT = '/usr/src/app/media'
    
# Media files configuration
MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Indicamos cual es el usuario por defecto de la aplicación
AUTH_USER_MODEL = 'usuarios.User'

# Configuración de urls de login
LOGIN_REDIRECT_URL = reverse_lazy('dashboard:index')
LOGIN_URL = reverse_lazy('login')
LOGOUT_URL = reverse_lazy('public:index')


# Configuración de email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env.get('EMAIL_HOST')
EMAIL_HOST_USER = env.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = int(env.get('EMAIL_PORT'))
EMAIL_USE_TLS = True

# Configuración para mantener el monitoreo de rendimiento de la app debug_toolbar
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]