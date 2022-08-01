from django.urls import path, include

from core.cursos.views import index


urlpatterns = [
    path('', index, name='index'),
    
]
