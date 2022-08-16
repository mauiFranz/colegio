from django.urls import path

from core.mensualidades.views import index


app_name = 'mensualidades'

urlpatterns = [
    path('', index, name='index')
]