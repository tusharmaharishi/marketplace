from rest_framework import serializers
from .models import User, Carpool
import uuid


class UserSerializer(serializers.ModelSerializer):
    id_user = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id_user', 'name', 'balance', 'carpool_owned', 'carpool_joined')


class CarpoolSerializer(serializers.ModelSerializer):
    id_carpool = serializers.CharField(read_only=True)

    class Meta:
        model = Carpool
        fields = ('id_carpool', 'driver', 'passengers', 'cost', 'location_start', 'location_end', 'time_leaving', 'time_arrival')

# class UserSerializer(serializers.Serializer):
#     id_user = serializers.UUIDField(required=True, format='hex')
#     name = serializers.CharField(required=True) # user's first and last name
#     balance = serializers.FloatField(default=10, min_value=0) # default to $0.00
#     carpool_owned = serializers.IntegerField(required=True) # only one carpool owned per user (driver) is id_carpool
#     carpool_joined = serializers.IntegerField(required=True) # only one carpool joined per user (rider) is id_carpool
#
#     def create(self, data):
#         """
#         :param data:
#         :return:
#         """
#         return User.objects.create(**data)
#
#
#     def update(self, instance, data):
#         """
#         :param instance:
#         :param data:
#         :return:
#         """
#         # instance.id_user = data.get('id_user', instance.id_user)
#         instance.name = data.get('name', instance.name)
#         instance.balance = data.get('balance', instance.balance)
#         instance.carpool_owned = data.get('carpool_owned', instance.carpool_owned)
#         instance.carpool_joined = data.get('carpool_joined', instance.carpool_joined)
#         instance.save()
#         return instance


# class CarpoolSerializer(serializers.Serializer):
#     # id_carpool = serializers.IntegerField(required=True)
#     driver = serializers.IntegerField(required=True)  # single driver (driver's id_user)
#     passengers = serializers.ListField(required=True,
#                                        child=serializers.IntegerField(required=True))  # multiple passengers (id_user)
#     cost = serializers.FloatField(default=2, min_value=0)
#     # is_full = serializers.BooleanField()
#     location_start = serializers.FloatField(default=18.18)
#     location_end = serializers.FloatField(default=12.02)
#     time_leaving = serializers.FloatField(default=11)
#     time_arrival = serializers.FloatField(default=13)
#
#     def create(self, data):
#         """
#         :param data:
#         :return:
#         """
#         return Carpool.objects.create(**data)
#
#     def update(self, instance, data):
#         instance.driver = data.get('driver', instance.driver)
#         instance.passengers = data.get('passengers', instance.passengers)
#         instance.cost = data.get('cost', instance.cost)
#         instance.location_start = dat
#         instance.location_end = serializers.CharField(required=True)
#         instance.time_leaving = serializers.CharField(required=True)
#         instance.time_arrival = serializers.CharField(required=True)
