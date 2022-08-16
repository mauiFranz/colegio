from django.urls import path, include

from core.agenda.views import index


urlpatterns = [
    path('', index, name='index'),
]
