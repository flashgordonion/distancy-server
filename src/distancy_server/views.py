from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from distancy_server import serializers
from distancy_server import models
from datetime import datetime, timedelta
from distancy_server import services
import pytz
import math


class ReservationSearch(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        qp = request.data

        if 'store_id' not in qp:
            raise(ValidationError(detail={'store_id': ["This field is required"]}))
        store_id = qp['store_id']
        store_conf = models.StoreCapacityConfig.objects.get(store=store_id)

        # Initially set start date to specified timerange
        start_search = services.read_dt_str(
            qp.get('search_date', datetime.utcnow().isoformat())
        )

        # Adjust to store opening time if store opening is greater
        opening_time = datetime.combine(start_search.date(), store_conf.opening_time)
        opening_time = pytz.utc.localize(opening_time)
        start_search = start_search if (start_search > opening_time) else opening_time

        # Use Ceiling of the slot so people don't miss their reservation
        time_till_d = (start_search - opening_time).seconds / 60
        time_to_add = math.ceil(time_till_d / store_conf.timeslot_duration)
        start_search = opening_time + timedelta(minutes=(time_to_add * store_conf.timeslot_duration))

        # Get End time such that
        hr_offset = qp.get('offset', 1)
        end_search = start_search + timedelta(hours=hr_offset)
        # TODO - if end time will be when when the store is closed set end date to closing time

        # Eventually we can put this into a django ORM function.  I don't know how to do that now
        def getslots(start_datetime: datetime, end_datetime: datetime, slot_size: int):
            num_slots = math.ceil((end_datetime - start_datetime).seconds / (60 * slot_size))
            for n in range(num_slots):
                arrival_start = start_datetime + timedelta(minutes=(n * slot_size))
                arrival_end = arrival_start + timedelta(minutes=slot_size)
                yield arrival_start, arrival_end
            pass

        slots = []
        for idx, (start, stop) in enumerate(getslots(start_search, end_search, store_conf.timeslot_duration)):
            res_slots = models.Reservation.objects \
                .filter(store=store_id) \
                .filter(slot_time=start)
            res_slot_len = len(res_slots)
            slots.append({
                "taken": res_slot_len,
                "maximum": store_conf.reservation_capacity,
                "arrive_after": start,
                "arrive_before": stop
            })

        return Response({"slots": slots})


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
        q_params = self.request.query_params

        qs = models.Reservation.objects.filter(user=requesting_user)
        if 'store' in q_params:
            qs = qs.filter(store=q_params['store'])
        if 'slot_time__gte' in q_params:
            slot_dt = services.read_dt_str( q_params['slot_time__gte'])
            qs = qs.filter(slot_time__gte=slot_dt)

        return qs
