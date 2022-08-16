from django.urls import path, include

from core.usuarios import views

app_name = 'usuarios'

urlpatterns = [
    path('list/', views.UserListView.as_view(), name='list'),
    path('create/', views.UserCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='update'),
    path('detail/<int:pk>/', views.UserDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', views.UserDeleteView.as_view(), name='delete'),
    path('roles_update/', views.RolesUpdateView.as_view(), name='roles_update'),
    path('provincias/', views.ProvinciaListView.as_view()),
    path('comunas/', views.ComunaListView.as_view()),
]
