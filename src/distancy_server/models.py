from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class User(AbstractUser):
    pass


class Store(models.Model):
    store_name = models.CharField(max_length=511, db_index=True)
    street_address = models.CharField(max_length=511, db_index=True)
    city = models.CharField(max_length=255, db_index=True)
    state = models.CharField(max_length=255, db_index=True)
    zip_code = models.CharField(max_length=255, db_index=True)


class StoreCapacityConfig(models.Model):
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    relevant_date = models.DateTimeField(null=False, blank=False, db_index=True)
    total_capacity = models.IntegerField(null=False, blank=False)
    reservation_capacity = models.IntegerField(null=False, blank=False)
    timeslot_duration = models.IntegerField(null=False, blank=False)
    opening_time = models.TimeField(null=False, blank=False)
    closing_time = models.TimeField(null=False, blank=False)


class Reservation(models.Model):
    store = models.ForeignKey('Store', on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)
    slot_time = models.DateTimeField(null=False, blank=False, db_index=True)
    slot_time_end = models.DateTimeField(null=False, blank=False, db_index=True)
