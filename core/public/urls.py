from django.urls import path, include

from core.public import views

app_name = 'public'

urlpatterns = [
    path('', views.IndexTemplate.as_view(), name='index'),
]
