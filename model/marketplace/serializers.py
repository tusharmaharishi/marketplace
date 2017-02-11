from rest_framework import serializers
from .models import User


class UserSerializer(serializers.Serializer):
    id_user = serializers.IntegerField(required=True) # TODO: make this read only, generate unique id, user shouldn't post it
    name = serializers.CharField(required=True)
    balance = serializers.CharField(required=True)
    carpool_owned = serializers.CharField(required=True)
    carpool_joined = serializers.CharField(required=True)

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
        instance.id_user = data.get('id_user', instance.id_user)
        instance.name = data.get('name', instance.name)
        instance.balance = data.get('balance', instance.balance)
        instance.carpool_owned = data.get('carpool_owned', instance.carpool_owned)
        instance.carpool_joined = data.get('carpool_joined', instance.carpool_joined)
        instance.save()
        return instance
