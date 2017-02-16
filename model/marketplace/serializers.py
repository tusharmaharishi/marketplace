from rest_framework import serializers
from .models import User, Carpool
import uuid


class UserSerializer(serializers.ModelSerializer):
    # id_user = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('name', 'balance', 'carpool_owned', 'carpool_joined')


class CarpoolSerializer(serializers.ModelSerializer):
    # id_carpool = serializers.CharField(read_only=True)

    class Meta:
        model = Carpool
        fields = ('driver', 'cost', 'location_start', 'location_end', 'time_leaving', 'time_arrival')