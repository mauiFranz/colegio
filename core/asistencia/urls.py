from django.urls import path, include

from core.asistencia.views import index


urlpatterns = [
    path('', index, name='index'),
]
