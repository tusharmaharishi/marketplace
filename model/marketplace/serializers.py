from rest_framework import serializers
from .models import User, Carpool
import uuid


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'balance')#, 'carpool_owned', 'carpool_joined')


class CarpoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carpool
        fields = ('id', 'driver', 'cost', 'location_start', 'location_end', 'time_leaving', 'time_arrival')
