from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from distancy_server import models
from datetime import datetime
import pytz


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = models.User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.get_or_create(user=user)
        return user

    class Meta:
        model = models.User
        fields = ['username', 'email', 'password', 'auth_token']
        extra_kwargs = {
            'password': {'write_only': True},
            'auth_token': {'read_only': True}
        }


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Store
        fields = '__all__'


class StoreCapacityConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreCapacityConfig
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=models.User, required=False)

    def validate(self, data):
        # We want to trust a users auth
        user = self.context['request'].user
        data['user'] = user

        store_conf = models.StoreCapacityConfig.objects.get(store=data['store'])
        timeslot_secs = 60 * store_conf.timeslot_duration

        # Ensure time slot aligns with allowed slot
        opening_time = datetime.combine(data['slot_time'].date(), store_conf.opening_time)
        opening_time = pytz.utc.localize(opening_time)
        if (data['slot_time'] - opening_time).seconds % timeslot_secs != 0:
            raise ValidationError(detail={'slot': 'time slot does not align'})

        # Ensure time slot is appropriate length
        if (data['slot_time_end'] - data['slot_time']).seconds != timeslot_secs:
            raise ValidationError(detail={'slot': 'time slot is not correct duration'})

        # Ensure time slot count won't exceed max allowed slots
        current_slot_q = models.Reservation.objects.filter(store=data['store'], slot_time=data['slot_time'])
        if current_slot_q.count() >= store_conf.reservation_capacity:
            raise ValidationError(detail={'slot': 'time slot at capacity'})

        # Ensure only one person has a reservation
        if current_slot_q.filter(user=user).exists():
            raise ValidationError(detail={'slot': 'user already has this time slot reserved'})

        # TODO - Ensure one person has one reservation at a given store per day

        return data

    class Meta:
        model = models.Reservation
        fields = '__all__'
