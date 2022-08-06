from rest_framework.viewsets import ModelViewSet


from core.usuarios import models
from core.usuarios.api import serializers


class UserModelViewSet(ModelViewSet):
    serializer_class = serializers.UserModelSerializers
    queryset = models.User.objects.all()
    

class RegionModelViewSet(ModelViewSet):
    serializer_class = serializers.RegionModelSerilizer
    http_method_names = ['get']
    queryset = models.Region.objects.all()
    
    
class ProvinciaModelViewSet(ModelViewSet):
    serializer_class = serializers.ProvinciaModelSerializer
    http_method_names = ['get']
    
    def get_queryset(self):
        id_region = self.request.GET.get('id_region', None)
        if not id_region:
            queryset = self.serializer_class.Meta.model.objects.all()
        else:
            queryset = self.serializer_class.Meta.model.objects.filter(region_provincia_id=id_region)
        return queryset


class ComunaModelViewSet(ModelViewSet):
    serializer_class = serializers.ComunaModelSerializer
    
    def get_queryset(self):
        
        queryset = super().get_queryset()
        queryset = queryset # TODO
        return queryset