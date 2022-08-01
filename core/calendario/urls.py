from django.urls import path, include

from core.calendario.views import index


urlpatterns = [
    path('', index, name='index'),
]
