import json

from django.core import serializers
from django.http import JsonResponse
from rest_framework.views import APIView

from .forms import UserForm, CarpoolForm
from .models import User, Carpool


def index(request):
    if request.method == 'GET':
        return JsonResponse({'status': '200 OK', 'message': 'This is the model API entry point.'}, status=200)


def get_user(pk):
    try:
        return User.objects.get(pk=pk)
    except User.DoesNotExist:
        return None


def get_carpool(pk):
    try:
        return Carpool.objects.get(pk=pk)
    except Carpool.DoesNotExist:
        return None


def update_user(form):
    response = {}
    if form.is_valid():
        user = form.save()
        if user.carpool_joined:
            carpool = get_carpool(pk=user.carpool_joined.pk)
            carpool.passengers.add(user)
            carpool.save()
        response['data'] = json.loads(serializers.serialize('json', [user, ]))
        response['status'] = '201 Created'
        return JsonResponse(response, status=201)
    else:
        response['status'] = '400 Bad Request'
        response['message'] = form.errors
        return JsonResponse(response, status=400)


def update_carpool(form):
    response = {}
    if form.is_valid():
        carpool = form.save()
        user = get_user(pk=carpool.driver.pk)
        user.carpool_owned = carpool
        if carpool.passengers:
            for user_pk in carpool.passengers.all():
                User.objects.filter(pk=user_pk).update(carpool_joined=carpool.pk)
        user.save()
        response['data'] = json.loads(serializers.serialize('json', [carpool, ]))
        response['status'] = '201 Created'
        return JsonResponse(response, status=201)
    else:
        response['status'] = '400 Bad Request'
        response['message'] = form.errors
        return JsonResponse(response, status=400)


class UserList(APIView):
    def get(self, request, **kwargs):
        if request.method == 'GET':
            users = User.objects.filter(**kwargs) if kwargs else User.objects.all()
            response = {}
            if users:
                response['data'] = json.loads(serializers.serialize('json', users))
                response['count'] = users.count()
                response['status'] = '200 OK'
                return JsonResponse(response, status=200)
            else:
                return JsonResponse({'status': '404 Not Found', 'message': 'These users do not exist.'}, status=404)

    def post(self, request):
        if request.method == 'POST':
            form = UserForm(request.data)
            return update_user(form=form)

    def delete(self, request):
        if request.method == 'DELETE':
            User.objects.all().delete()
            return JsonResponse({'status': '204 No Content'}, status=204)


class UserDetail(APIView):
    def get(self, request, pk):
        if request.method == 'GET':
            user = get_user(pk=pk)
            response = {}
            if user is not None:
                response['data'] = json.loads(serializers.serialize('json', [user, ]))
                response['count'] = 1
                response['status'] = '200 OK'
                return JsonResponse(response, status=200)
            else:
                return JsonResponse({'status': '404 Not Found', 'message': 'This user does not exist.'}, status=404)

    def put(self, request, pk):
        if request.method == 'PUT':
            user = get_user(pk=pk)
            if user is not None:
                form = UserForm(request.data, instance=user)
                return update_user(form=form)
            else:
                return JsonResponse({'status': '404 Not Found', 'message': 'This user does not exist.'}, status=404)

    def delete(self, request, pk):
        if request.method == 'DELETE':
            user = get_user(pk=pk)
            if user is not None:
                user.delete()
                return JsonResponse({'status': '204 No Content'}, status=204)
            else:
                return JsonResponse({'status': '404 Not Found', 'message': 'This user does not exist.'}, status=404)


class CarpoolList(APIView):
    def get(self, request, **kwargs):
        if request.method == 'GET':
            carpools = Carpool.objects.filter(**kwargs) if kwargs else Carpool.objects.all()
            response = {}
            if carpools:
                response['data'] = json.loads(serializers.serialize('json', carpools))
                response['count'] = carpools.count()
                response['status'] = '200 OK'
                return JsonResponse(response, status=200)
            else:
                return JsonResponse({'status': '404 Not Found', 'message': 'These carpools do not exist.'}, status=404)

    def post(self, request):
        if request.method == 'POST':
            form = CarpoolForm(request.data)
            return update_carpool(form=form)

    def delete(self, request):
        if request.method == 'DELETE':
            Carpool.objects.all().delete()
            return JsonResponse({'status': '204 No Content'}, status=204)


class CarpoolDetail(APIView):
    def get(self, request, pk):
        if request.method == 'GET':
            carpool = get_carpool(pk=pk)
            response = {}
            if carpool is not None:
                response['data'] = json.loads(serializers.serialize('json', [carpool, ]))
                response['count'] = 1
                response['status'] = '200 OK'
                return JsonResponse(response, status=200)
            else:
                return JsonResponse({'status': '404 Not Found', 'message': 'This carpool does not exist.'}, status=404)

    def put(self, request, pk):
        if request.method == 'PUT':
            carpool = get_carpool(pk=pk)
            if carpool is not None:
                form = CarpoolForm(request.data, instance=carpool)
                return update_carpool(form=form)
            else:
                return JsonResponse({'status': '404 Not Found', 'message': 'This carpool does not exist.'}, status=404)

    def delete(self, request, pk):
        if request.method == 'DELETE':
            carpool = get_carpool(pk=pk)
            if carpool is not None:
                carpool.delete()
                return JsonResponse({'status': '204 No Content'}, status=204)
            else:
                return JsonResponse({'status': '404 Not Found', 'message': 'This carpool does not exist.'}, status=404)
