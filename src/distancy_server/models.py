from django.db import models


class Store(models.Model):
    store_name = models.CharField(max_length=511)
    street_address = models.CharField(max_length=511)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)


class StoreCapacityConfig(models.Model):
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    relevant_date = models.DateTimeField(null=False, blank=False, db_index=True)
    total_capacity = models.IntegerField(null=False, blank=False)
    reservation_capacity = models.IntegerField(null=False, blank=False)
    timeslot_duration = models.IntegerField(null=False, blank=False)
    opening_time = models.TimeField(null=False, blank=False)
    closing_time = models.TimeField(null=False, blank=False)


class Reservation(models.Model):
    pass

