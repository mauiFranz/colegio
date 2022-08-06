"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', include('core.public.urls')),
    path('dash/', include('core.dash.urls')),
    path('agenda/', include('core.agenda.urls')),
    path('usuarios/', include('core.usuarios.urls')),
    path('asistencia/', include('core.asistencia.urls')),
    path('cursos/', include('core.cursos.urls')),
    path('calendario/', include('core.calendario.urls')),
    path('asignaturas/', include('core.asignaturas.urls')),
    path('libro-clases/', include('core.libro_clases.urls')),
    path('mensualidades/', include('core.mensualidades.urls')),
    
    # API URLS
    # path('api/v1/', include('core.usuarios.api.routers')),
]
