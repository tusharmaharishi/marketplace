from django.db import models


class User(models.Model):
    id_user = models.TextField()
    name = models.TextField()
    balance = models.TextField()
    carpool_owned = models.TextField()
    carpool_joined = models.TextField()


# class Carpool(models.Model):
#     id_carpool = models.TextField()
#     driver = models.TextField()  # single driver (user)
#     passengers = models.TextField()  # list of passengers (users)
#     cost = models.TextField()
#     location_start = models.TextField()
#     location_end = models.TextField()
#     time_leaving = models.TextField()
#     time_arrival = models.TextField()
