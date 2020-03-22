from rest_framework import serializers
from distancy_server import models


class StoreCapacityConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreCapacityConfig
        fields = '__all__'