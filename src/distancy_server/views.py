from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from distancy_server import serializers
from distancy_server import models


class StoreCapacityConfigViewSet(ModelViewSet):
    serializer_class = serializers.StoreCapacityConfigSerializer
    queryset = models.StoreCapacityConfig.objects.all()
