from .models import User, Carpool
from .serializers import UserSerializer, CarpoolSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse


def hello_world(request):
    return render(request, 'marketplace/hello_world.html', {})


class UserList(APIView):

    def get(self, request):
        users = User.objects.all()  # TODO: get all users returns integer error '',
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=200, content_type='application/json')

    def post(self, request):
        serializer = UserSerializer(data=request.data)  # TODO: don't allow duplicate posts, permissions auth
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201, content_type='application/json')
        return Response(serializer.errors, status=400)


class UserDetail(APIView):

    def get_user(self, id_user):
        try:
            return User.objects.get(id_user=id_user)
        except User.DoesNotExist:
            raise Response(status=404)

    def get(self, request, id_user):
        user = self.get_user(id_user=id_user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200, content_type='application/json')

    def put(self, request, id_user):
        user = self.get_user(id_user=id_user)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201, content_type='application/json')
        return Response(serializer.errors, status=400)

    def delete(self, request, id_user):
        user = self.get_user(id_user=id_user)
        user.delete()
        return Response(status=204)


class CarpoolList(APIView):
    def get(self, request):
        carpools = Carpool.objects.all()
        serializer = CarpoolSerializer(carpools, many=True)
        return Response(serializer.data, status=200, content_type='application/json')

    def post(self, request):
        serializer = CarpoolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201, content_type='application/json')
        return Response(serializer.errors, status=400)


class CarpoolDetail(APIView):
    def get_carpool(self, id_carpool):
        try:
            return Carpool.bojects.get(id_carpool=id_carpool)
        except Carpool.DoesNotExist:
            raise Response(status=404)

    def get(self, request, id_carpool):
        carpool = self.get_carpool(id_carpool=id_carpool)
        serializer = UserSerializer(carpool)
        return Response(serializer.data, status=200, content_type='application/json')

    def put(self, request, id_carpool):
        carpool = self.get_carpool(id_carpool=id_carpool)
        serializer = UserSerializer(carpool, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201, content_type='application/json')
        return Response(serializer.errors, status=400)

    def delete(self, request, id_carpool):
        carpool = self.get_user(id_user=id_carpool)
        carpool.delete()
        return Response(status=204)
