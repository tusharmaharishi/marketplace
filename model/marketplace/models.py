from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=128)
    username = models.CharField(max_length=128, default="username")
    password = models.CharField(max_length=128, default="password")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)])
    carpool_owned = models.ForeignKey(  # user is driver, user deletes himself, carpool is deleted
        'Carpool',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='driver_set'
    )
    carpool_joined = models.ForeignKey(  # user is passenger, user deletes himself, carpool is still there
        'Carpool',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='passenger_set'
    )


class Carpool(models.Model):
    driver = models.ForeignKey(  # carpool is deleted, driver should not delete himself
        'User',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='carpool_owned_set'
    )  # single driver per carpool (user)
    passengers = models.ManyToManyField(
        'User',
        related_name='carpool_joined_set',
        blank=True
    )  # list of multiple passengers per carpool (users)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=1.50, validators=[MinValueValidator(0)])
    location_start_lat = models.FloatField(default=38.037658, validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    location_start_lon = models.FloatField(default=-78.485381, validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])
    location_end_lat = models.FloatField(default=38.037658, validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    location_end_lon = models.FloatField(default=-78.485381, validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])
    time_leaving = models.DateTimeField()
    time_arrival = models.DateTimeField()


class Authenticator(models.Model):
    username = models.CharField(max_length=128)
    authenticator = models.CharField(max_length=255, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
