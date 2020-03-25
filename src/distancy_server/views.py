from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from distancy_server import serializers
from distancy_server import models


class ReservationSearch(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        openSlots = {
            'TODO 1': 'Filter Reservations Matching Store',
            'TODO 2': 'Filter Reservations Starting after Start Time',
            'TODO 3': 'FROM QUERY Params determine end time',
            'TODO 4': 'Filter Reservations before end time',
            'TODO 5': 'Apply a list Serializer to limit the number of records',
            'TODO 5a': 'limit date range to 1 day to prevent overfetching',
            'TODO 6': 'PHASE 2: paginate results when people select a wide swath'
        }
        # Select all where matching store and

        return Response(openSlots)


class TokenValidationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        user = request.user
        user_data = serializers.UserSerializer(user).data
        return Response(user_data)


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
