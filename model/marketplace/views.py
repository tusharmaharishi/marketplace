from django.core import serializers
from django.http import JsonResponse
from rest_framework.views import APIView

from .forms import UserForm
from .models import User, Carpool


def index(request):
    if request.method == 'GET':
        return JsonResponse({"message": "Model API entry point"}, status=200)


class UserList(APIView):
    def get(self, request):
        if request.method == 'GET':
            users = User.objects.all()
            response = {}
            response['status'] = '200 OK'
            response['data'] = {}
            response['data']['count'] = users.count()
            response['data']['users'] = serializers.serialize('json', users)
            return JsonResponse(response, status=200)

    def post(self, request):
        if request.method == 'POST':
            form = UserForm(request.data)
            response = {}
            if form.is_valid():
                form.save()
                response['status'] = '201 Created'
                response['data'] = serializers.serialize('json', [form, ])
                return JsonResponse(response, status=201)
            else:
                response['status'] = '400 Bad Request'
                response['message'] = form.errors
                return JsonResponse(response, status=400)

    def delete(self, request):
        if request.method == 'DELETE':
            User.objects.all().delete()
            return JsonResponse({'status': '204 No Content'}, status=204)


class UserDetailById(APIView):
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            response = {}
            response['status'] = '404 Not Found'
            response['message'] = 'User with id "' + pk + '" does not exist'
            return JsonResponse(response, status=404)

    def get(self, request, pk):
        if request.method == 'GET':
            user = self.get_user(pk=pk)
            response = {}
            response['status'] = '200 OK'
            response['data'] = {}
            response['data']['count'] = 1
            response['data']['users'] = serializers.serialize('json', user)
            return JsonResponse(response, status=200)

    def put(self, request, pk):
        if request.method == 'PUT':
            user = self.get_user(pk=pk)
            form = UserForm(request.data, instance=user)
            response = {}
            if form.is_valid():
                form.save()
                response['status'] = '201 Created'
                response['data'] = serializers.serialize('json', [form, ])
                return JsonResponse(response, status=201)
            else:
                response['status'] = '400 Bad Request'
                response['message'] = form.errors
                return JsonResponse(response, status=400)

    def delete(self, request, pk):
        if request.method == 'DELETE':
            user = self.get_user(pk=pk)
            user.delete()
            return JsonResponse({'status': '204 No Content'}, status=204)


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


class CarpoolDetailById(APIView):
    def get_carpool(self, pk):
        try:
            return Carpool.objects.get(pk=pk)
        except Carpool.DoesNotExist:
            return JsonResponse({"message": "User does not exist"})

    def get(self, request, pk):
        carpool = self.get_carpool(pk=pk)
        serializer = CarpoolSerializer(carpool, many=True)
        return Response(serializer.data, status=200, content_type='application/json')

    def put(self, request, pk):
        carpool = self.get_carpool(pk=pk)
        serializer = CarpoolSerializer(carpool, many=True, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201, content_type='application/json')
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        carpool = self.get_carpool(pk=pk)
        carpool.delete()
        return Response(status=204)

