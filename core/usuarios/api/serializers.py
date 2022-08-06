from rest_framework import serializers

from core.usuarios import models


class UserModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'
        
    def create(self, validated_data):
        user = models.User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        update_user = super().update(instance, validated_data)
        update_user.set_password(validated_data['password'])
        update_user.save()
        return update_user
    

class RegionModelSerilizer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        fields = '__all__'
        
        
class ProvinciaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provincia
        fields = '__all__'
        

class ComunaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comuna
        fields = '__all__'