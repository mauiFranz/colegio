from django.urls import path, include

from core.asignaturas.views import index


urlpatterns = [
    path('', index, name='index'),
]
