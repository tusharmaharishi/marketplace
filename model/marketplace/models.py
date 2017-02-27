from django.db import models


class Carpool(models.Model):
    driver = models.ForeignKey(  # carpool is deleted, driver should not delete himself
        'User',
        on_delete=models.CASCADE,
        related_name='+'
    )  # single driver per carpool (user)
    passengers = models.ManyToManyField(
        'User',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='+'
    )  # list of multiple passengers per carpool (users)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=1.50)
    location_start = models.FloatField(default=8.8)
    location_end = models.FloatField(default=8.8)
    time_leaving = models.FloatField(default=8.8)
    time_arrival = models.FloatField(default=8.8)

    def __str__(self):
        return self.driver + "'s Carpool"


class User(models.Model):
    name = models.CharField(max_length=128)
    # username = models.CharField(max_length=128)
    # password = models.CharField(max_length=128)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    carpool_owned = models.ForeignKey(  # user is driver, user deletes himself, carpool is deleted
        Carpool,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='+'
    )
    carpool_joined = models.ForeignKey(  # user is passenger, user deletes himself, carpool is still there
        Carpool,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='+'
    )

    def __str__(self):
        return self.name
