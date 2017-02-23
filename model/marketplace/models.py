from django.db import models
import uuid


class User(models.Model):
    # id_user = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=128)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
#    carpool_owned = models.OneToOneField(  # user is driver, user deletes himself, carpool is deleted
#        'Carpool',
#        on_delete=models.CASCADE,
#        blank=True,
#        null=True,
#        related_name='carpool_driver',
#    )
#    carpool_joined = models.ForeignKey(  # user is passenger, user deletes himself, carpool is still there
#        'Carpool',
#        on_delete=models.CASCADE,
#        blank=True,
#        null=True,
#        related_name='carpool_passenger'
#    )

class Carpool(models.Model):
    # id_carpool = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.AutoField(primary_key=True, editable=False)
    driver = models.ForeignKey( #carpool is deleted, driver should not delete himself 
        User,
        on_delete=models.CASCADE,
        blank=True,
        related_name='+'
        )  # single driver per carpool (user)
    
    # passengers = models.ManyToManyField(
    #     'User',
    #     blank=True,
    #     null=True
    # )  # list of multiple passengers per carpool (users)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=1.50)
    location_start = models.FloatField(default=8.8)
    location_end = models.FloatField(default=8.8)
    time_leaving = models.FloatField(default=8.8)
    time_arrival = models.FloatField(default=8.8)
