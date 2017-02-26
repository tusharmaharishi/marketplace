from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Carpool
from .serializers import UserSerializer, CarpoolSerializer


def index(request):
    return HttpResponse("Model API", status=200)


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
    def get_user(self, id):
        try:
            return User.objects.filter(id=id)
        except User.DoesNotExist:
            raise Response(status=404)

    def get(self, request, id):
        user = self.get_user(id=id)
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=200, content_type='application/json')

    def put(self, request, id):
        user = self.get_user(id=id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201, content_type='application/json')
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        user = self.get_user(id=id)
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
    def get_carpool(self, id):
        try:
            return Carpool.objects.filter(id=id)
        except Carpool.DoesNotExist:
            raise Response(status=404)

    def get(self, request, id):
        carpool = self.get_carpool(id=id)
        serializer = CarpoolSerializer(carpool, many=True)
        return Response(serializer.data, status=200, content_type='application/json')

    def put(self, request, id):
        carpool = self.get_carpool(id=id)
        serializer = CarpoolSerializer(carpool, many=True, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201, content_type='application/json')
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        carpool = self.get_carpool(id=id)
        carpool.delete()
        return Response(status=204)
