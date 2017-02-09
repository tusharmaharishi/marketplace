from rest_framework import serializers
from marketplace.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'user_id', 'balance')
