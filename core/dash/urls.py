from django.urls import path

from core.dash import views


app_name = 'dashboard'

urlpatterns = [
    path('', views.DashTemplateView.as_view(), name='index')
]