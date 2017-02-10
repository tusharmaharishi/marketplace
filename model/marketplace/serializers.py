from rest_framework import serializers
from .models import User


class UserSerializer(serializers.Serializer):
    id_user = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    balance = serializers.IntegerField(required=True)
    carpool_owned = serializers.IntegerField()
    carpool_joined = serializers.IntegerField()

    def create(self, data):
        """
        :param data:
        :return:
        """
        return User.objects.create(**data)


    def update(self, instance, data):
        """
        :param instance:
        :param data:
        :return:
        """
        instance.name = data.get('name', instance.name)
        instance.balance = data.get('balance', instance.balance)
        instance.carpool_owned = data.get('carpool_owned', instance.carpool_owned)
        instance.carpool_joined = data.get('carpool_joined', instance.carpool_joined)
        instance.save()
        return instance
