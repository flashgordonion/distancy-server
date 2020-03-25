from rest_framework import serializers
from distancy_server import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username']


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
        user = self.context['request'].user
        data['user'] = user

        # TODO Ensure this request doesn't make more than reserved capacity in given slot
        return data

    class Meta:
        model = models.Reservation
        fields = '__all__'
