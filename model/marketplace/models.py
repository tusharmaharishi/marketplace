from django.db import models
import uuid

class User(models.Model):
    id_user = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    carpool_owned = models.OneToOneField(  # user is driver, user deletes himself, carpool is deleted
        'Carpool',
        to_field='id_carpool',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='carpool_driver',
    )
    carpool_joined = models.ForeignKey(  # user is passenger, user deletes himself, carpool is still there
        'Carpool',
        to_field='id_carpool',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='carpool_passenger'
    )


class Carpool(models.Model):
    id_carpool = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    driver = models.OneToOneField(  # carpool is deleted, but driver should not delete himself (form new carpool)
        'User',
        to_field='id_user',
        on_delete=models.CASCADE,
        blank=True,
        related_name='+'
    )  # single driver per carpool (user)
    passengers = models.ManyToManyField(User)  # list of multiple passengers per carpool (users)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    location_start = models.FloatField(default=8.8)
    location_end = models.FloatField(default=8.8)
    time_leaving = models.FloatField(default=8.8)
    time_arrival = models.FloatField(default=8.8)
