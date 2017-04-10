from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models

name_validator = RegexValidator(regex=r"^[A-Za-z]([-']?[a-z]+)*( [A-Za-z]([-']?[a-z]+)*)+$")  # full name requires space
username_validator = RegexValidator(regex=r"^(?=.{4,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$")  # 8-20 chars
# pbkdf2_sha256_validator = RegexValidator(regex=r"^$pbkdf2-sha256")
sha256_validator = RegexValidator(regex=r"[A-Fa-f0-9]{64}")  # sha256 hash is 64 bytes long


class User(models.Model):
    name = models.CharField(max_length=128, validators=[name_validator])
    username = models.CharField(max_length=128, default='username', validators=[username_validator])
    password = models.CharField(max_length=255,
                                default="$pbkdf2-sha256$6400$.6UI/S.nXIk8jcbdHx3Fhg$98jZicV16ODfEsEZeYPGHU3kbrUrvUEXOPimVSQDD44")  # password uses PBKDF2 hashes to sha256
    balance = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
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
    cost = models.DecimalField(default=1.50, max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    location_start_lat = models.FloatField(default=38.037658,
                                           validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    location_start_lon = models.FloatField(default=-78.485381,
                                           validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])
    location_end_lat = models.FloatField(default=38.037658,
                                         validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    location_end_lon = models.FloatField(default=-78.485381,
                                         validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])
    time_leaving = models.DateTimeField()
    time_arrival = models.DateTimeField()


class Authenticator(models.Model):
    username = models.CharField(max_length=128, default='username', validators=[username_validator])
    auth_token = models.CharField(max_length=255, primary_key=True, validators=[sha256_validator])
    date_created = models.DateTimeField(auto_now_add=True)
