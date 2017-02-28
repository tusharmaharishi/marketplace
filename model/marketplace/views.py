import json

from django.core import serializers
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView

from .forms import UserForm, CarpoolForm
from .models import User, Carpool


def index(request):
    if request.method == 'GET':
        return JsonResponse({"message": "Model API entry point"}, status=200)


def get_user(pk):
    try:
        return User.objects.get(pk=pk)
    except ObjectDoesNotExist:
        response = {}
        response['status'] = '404 Not Found'
        response['message'] = 'User with id "' + pk + '" does not exist'
        return JsonResponse(response, safe=False, status=404)


def get_carpool(pk):
    try:
        return Carpool.objects.get(pk=pk)
    except ObjectDoesNotExist:
        response = {}
        response['status'] = '404 Not Found'
        response['message'] = 'Carpool with id "' + pk + '" does not exist'
        return JsonResponse(response, status=404)


def update_user(form):
    response = {}
    if form.is_valid():
        user = form.save()
        if user.carpool_joined:
            carpool = get_carpool(pk=user.carpool_joined.pk)
            carpool.passengers.add(user)
            carpool.save()
        response['status'] = '201 Created'
        response['data'] = json.loads(serializers.serialize('json', [user, ]))
        return JsonResponse(response, status=201)
    else:
        response['status'] = '400 Bad Request'
        response['message'] = form.errors
        return JsonResponse(response, status=400)


def update_carpool(form):
    response = {}
    if form.is_valid():
        carpool = form.save()  # TODO: check carpool.driver is valid
        user = get_user(pk=carpool.driver.pk)
        user.carpool_owned = carpool
        if carpool.passengers:
            for user_pk in carpool.passengers.all():
                User.objects.filter(pk=user_pk).update(carpool_joined=carpool.pk)
        user.save()
        response['status'] = '201 Created'
        response['data'] = json.loads(serializers.serialize('json', [carpool, ]))
        return JsonResponse(response, status=201)
    else:
        response['status'] = '400 Bad Request'
        response['message'] = form.errors
        return JsonResponse(response, status=400)


class UserList(APIView):
    def get(self, request):
        if request.method == 'GET':
            users = User.objects.all()
            response = {}
            response['status'] = '200 OK'
            response['count'] = users.count()
            response['data'] = json.loads(serializers.serialize('json', users))
            return JsonResponse(response, status=200)

    def post(self, request):
        if request.method == 'POST':
            form = UserForm(request.data)
            return update_user(form=form)

    def delete(self, request):
        if request.method == 'DELETE':
            User.objects.all().delete()
            return JsonResponse({'status': '204 No Content'}, status=204)


class UserDetailById(APIView):
    def get(self, request, pk):
        if request.method == 'GET':
            user = get_user(pk=pk)
            response = {}
            response['status'] = '200 OK'
            response['count'] = 1
            response['data'] = json.loads(serializers.serialize('json', [user, ]))
            return JsonResponse(response, status=200)

    def put(self, request, pk):
        if request.method == 'PUT':
            user = get_user(pk=pk)
            form = UserForm(request.data, instance=user)
            return update_user(form=form)

    def delete(self, request, pk):
        if request.method == 'DELETE':
            user = get_user(pk=pk)
            user.delete()
            return JsonResponse({'status': '204 No Content'}, status=204)


class CarpoolList(APIView):
    def get(self, request):
        if request.method == 'GET':
            carpools = Carpool.objects.all()
            response = {}
            response['status'] = '200 OK'
            response['count'] = carpools.count()
            response['data'] = json.loads(serializers.serialize('json', carpools))
            return JsonResponse(response, status=200)

    def post(self, request):
        if request.method == 'POST':
            form = CarpoolForm(request.data)
            return update_carpool(form=form)

    def delete(self, request):
        if request.method == 'DELETE':
            Carpool.objects.all().delete()
            return JsonResponse({'status': '204 No Content'}, status=204)


class CarpoolDetailById(APIView):
    def get(self, request, pk):
        if request.method == 'GET':
            carpool = get_carpool(pk=pk)
            response = {}
            response['status'] = '200 OK'
            response['count'] = 1
            response['data'] = json.loads(serializers.serialize('json', [carpool, ]))
            return JsonResponse(response, status=200)

    def put(self, request, pk):
        if request.method == 'PUT':
            carpool = get_carpool(pk=pk)
            form = CarpoolForm(request.data, instance=carpool)
            return update_carpool(form=form)

    def delete(self, request, pk):
        if request.method == 'DELETE':
            carpool = get_carpool(pk=pk)
            carpool.delete()
            return JsonResponse({'status': '204 No Content'}, status=204)
