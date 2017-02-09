from django.db import models

# Create your models here.

class User(models.Model):
    name = models.TextField()
    user_id = models.TextField()

class Carpool(models.Model):
    carpool_id = models.TextField()
    driver = models.TextField() #single driver (user)
    passengers = models.TextField() #list of passengers (users)
    cost = models.TextField()
    location_start = models.TextField()
    location_end = models.TextField()

