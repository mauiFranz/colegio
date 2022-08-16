from rest_framework.routers import DefaultRouter

from core.usuarios.api import viewsets

router = DefaultRouter()
router.register(r'usuarios',viewsets.UserModelViewSet, basename='usuarios')
router.register(r'regiones', viewsets.RegionModelViewSet, basename='regiones')
router.register(r'provincias', viewsets.ProvinciaModelViewSet, basename='provincias')


urlpatterns = router.urls