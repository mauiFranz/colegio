from django.urls import path, include

from core.usuarios import views

app_name = 'usuarios'

urlpatterns = [
    path('list/', views.UserListView.as_view(), name='list'),
    path('create/', views.UserCreateView.as_view(), name='create'),
    path('provincias/', views.ProvinciaListView.as_view()),
    path('comunas/', views.ComunaListView.as_view()),
]
