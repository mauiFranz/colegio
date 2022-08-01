from django.urls import path, include

from core.libro_clases.views import index


urlpatterns = [
    path('', index, name='index'),
    
]
