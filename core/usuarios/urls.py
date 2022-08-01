from django.urls import path, include

from core.usuarios.views import index

urlpatterns = [
    path('', index, name='index'),    
]
