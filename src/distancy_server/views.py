from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from distancy_server import serializers
from distancy_server import models


class StoreCapacityConfigViewSet(ModelViewSet):
    serializer_class = serializers.StoreCapacityConfigSerializer
    queryset = models.StoreCapacityConfig.objects.all()


class StoreViewSet(ModelViewSet):
    serializer_class = serializers.StoreSerializer
    queryset = models.Store.objects.all()


class ReservationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ReservationSerializer

    def get_queryset(self):
        requesting_user = self.request.user
        qs = models.Reservation.objects.filter(user=requesting_user)
        return qs
