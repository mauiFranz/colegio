from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', include('core.public.urls')),
    path('dash/', include('core.dash.urls')),
    path('agenda/', include('core.agenda.urls')),
    path('dash/usuarios/', include('core.usuarios.urls')),
    path('dash/asistencia/', include('core.asistencia.urls')),
    path('dash/cursos/', include('core.cursos.urls')),
    path('dash/calendario/', include('core.calendario.urls')),
    path('dash/asignaturas/', include('core.asignaturas.urls')),
    path('dash/libro-clases/', include('core.libro_clases.urls')),
    path('dash/mensualidades/', include('core.mensualidades.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    
    # API URLS
    # path('api/v1/', include('core.usuarios.api.routers')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)