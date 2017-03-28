import hmac
import json
import os
from datetime import datetime

from django.conf import settings
from django.contrib.auth import hashers
from django.core import serializers
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.views import APIView

from .forms import UserForm, CarpoolForm, AuthenticatorForm, UserLoginForm
from .models import User, Carpool, Authenticator


def index(request):
    if request.method == 'GET':
        return JsonResponse({'status': 200, 'detail': 'This is the model API entry point.'}, status=200)


def get_auth(authenticator=None, username=None):
    if authenticator:
        try:
            return Authenticator.objects.get(authenticator=authenticator)
        except Authenticator.DoesNotExist:
            return None
    if username:
        try:
            return Authenticator.objects.get(username=username)
        except Authenticator.DoesNotExist:
            return None


def get_user(pk=None, username=None):
    if pk:
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
    if username:
        try:
            return User.objects.get(username=username)
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
        user = form.save(commit=False)
        user.password = hashers.make_password(password=user.password)
        user.save()
        if user.carpool_joined:
            carpool = get_carpool(pk=user.carpool_joined.pk)
            carpool.passengers.add(user)
            carpool.save()
        response['data'] = json.loads(serializers.serialize('json', [user, ]))
        response['status'] = 201
        return JsonResponse(response, status=201)
    else:
        response['status'] = 400
        response['detail'] = form.errors
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
        response['status'] = 201
        return JsonResponse(response, status=201)
    else:
        response['status'] = 400
        response['detail'] = form.errors
        return JsonResponse(response, status=400)


class UserList(APIView):
    def get(self, request, **kwargs):
        if request.method == 'GET':
            users = User.objects.filter(**kwargs) if kwargs else User.objects.all()
            response = {}
            if users:
                response['data'] = json.loads(serializers.serialize('json', users))
                response['count'] = users.count()
                response['status'] = 200
                return JsonResponse(response, status=200)
            else:
                return JsonResponse({'status': 404, 'detail': 'These users do not exist.'}, status=404)

    def post(self, request):
        if request.method == 'POST':
            if User.objects.filter(username=request.POST['username']).exists():
                return JsonResponse({'detail': 'This username already exists. Please choose another one.'}, status=400)
            form = UserForm(request.POST)
            return update_user(form=form)

    def delete(self, request):
        if request.method == 'DELETE':
            User.objects.all().delete()
            return JsonResponse({'status': 204}, status=204)


class UserDetail(APIView):
    def get(self, request, pk=None, username=None):
        if request.method == 'GET':
            user = None
            if pk:
                user = get_user(pk=pk)
            elif username:
                user = get_user(username=username)
            response = {}
            if user:
                response['data'] = json.loads(serializers.serialize('json', [user, ]))
                response['count'] = 1
                response['status'] = 200
                return JsonResponse(response, status=200)
            else:
                return JsonResponse({'status': 404, 'detail': 'This user does not exist.'}, status=404)

    def put(self, request, pk=None, username=None):
        if request.method == 'PUT':
            user = None
            if pk:
                user = get_user(pk=pk)
            elif username:
                user = get_user(username=username)
            if user:
                form = UserForm(request.data, instance=user)
                return update_user(form=form)
            else:
                return JsonResponse({'status': 404, 'detail': 'This user does not exist.'}, status=404)

    def delete(self, request, pk=None, username=None):
        if request.method == 'DELETE':
            user = None
            if pk:
                user = get_user(pk=pk)
            elif username:
                user = get_user(username=username)
            if user:
                user.delete()
                return JsonResponse({'status': 204}, status=204)
            else:
                return JsonResponse({'status': 404, 'detail': 'This user does not exist.'}, status=404)


class Authentication(APIView):
    def post(self, request):
        if request.method == 'POST':
            form = UserLoginForm(request.POST)  # validate user input when creating authentication
            if form.is_valid():
                # print(form.cleaned_data)
                user = get_user(username=form.cleaned_data['username'])
                if not user:
                    return JsonResponse({'status': 404, 'detail': 'This username does not exist.'}, status=404)
                response = {}
                token = get_auth(username=form.cleaned_data['username'])
                print(hashers.check_password(form.cleaned_data['password'], user.password))
                if token:
                    response['auth'] = token.authenticator
                    response['status'] = 409
                    response['detail'] = 'This authenticator already exists.'
                    return JsonResponse(response, status=409)
                elif hashers.check_password(form.cleaned_data['password'], user.password):
                    auth = hmac.new(
                        key=settings.SECRET_KEY.encode('utf-8'),
                        msg=os.urandom(32),
                        digestmod='sha256',
                    ).hexdigest()
                    token = AuthenticatorForm({'username': form.cleaned_data['username'],
                                               'authenticator': auth,
                                               'date_created': datetime.now()})
                    token.save()
                    response['auth'] = auth
                    response['status'] = 201
                    response['detail'] = 'Authenticator was successfully created for {}.'.format(
                        form.cleaned_data['username'])
                    return JsonResponse(response, status=201)
                else:
                    response['status'] = 400
                    response['detail'] = 'Authenticator was not created.'
                    return JsonResponse(response, status=400)


class AuthenticationCheck(APIView):
    def get(self, request, username=None, authenticator=None):
        if request.method == 'GET':
            token = None
            if username:
                token = get_auth(username=username)
            if authenticator:
                token = get_auth(authenticator=authenticator)
            response = {}
            if token:
                time_delta = (timezone.now() - token.date_created).days * 24 * 60
                if time_delta <= 120:  # token cannot be longer than two hours
                    response['auth'] = token.authenticator
                    response['status'] = 200
                    response['detail'] = 'Authenticator is valid.'
                    return JsonResponse(response, status=200)
                else:
                    response['status'] = 404
                    response['detail'] = 'Authenticator expired.'
                    return JsonResponse(response, status=404)
            else:
                return JsonResponse({'status': 404, 'detail': 'This authenticator does not exist.'},
                                    status=404)

    def delete(self, request, username=None, authenticator=None):
        if request.method == 'DELETE':
            token = None
            if username:
                token = get_auth(username=username)
            if authenticator:
                token = get_auth(authenticator=authenticator)
            if token:
                token.delete()
                return JsonResponse({'status': 204}, status=204)
            else:
                return JsonResponse({'status': 404, 'detail': 'This authenticator does not exist.'},
                                    status=404)


class CarpoolList(APIView):
    def get(self, request, **kwargs):
        if request.method == 'GET':
            carpools = Carpool.objects.filter(**kwargs) if kwargs else Carpool.objects.all()
            response = {}
            if carpools:
                response['data'] = json.loads(serializers.serialize('json', carpools))
                response['count'] = carpools.count()
                response['status'] = 200
                return JsonResponse(response, status=200)
            else:
                return JsonResponse({'status': 404, 'detail': 'These carpools do not exist.'}, status=404)

    def post(self, request):
        if request.method == 'POST':
            form = CarpoolForm(request.POST)
            return update_carpool(form=form)

    def delete(self, request):
        if request.method == 'DELETE':
            Carpool.objects.all().delete()
            return JsonResponse({'status': 204}, status=204)


class CarpoolDetail(APIView):
    def get(self, request, pk):
        if request.method == 'GET':
            carpool = get_carpool(pk=pk)
            response = {}
            if carpool:
                response['data'] = json.loads(serializers.serialize('json', [carpool, ]))
                response['count'] = 1
                response['status'] = 200
                return JsonResponse(response, status=200)
            else:
                return JsonResponse({'status': 404, 'detail': 'This carpool does not exist.'}, status=404)

    def put(self, request, pk):
        if request.method == 'PUT':
            carpool = get_carpool(pk=pk)
            if carpool:
                form = CarpoolForm(request.data, instance=carpool)
                return update_carpool(form=form)
            else:
                return JsonResponse({'status': 404, 'detail': 'This carpool does not exist.'}, status=404)

    def delete(self, request, pk):
        if request.method == 'DELETE':
            carpool = get_carpool(pk=pk)
            if carpool:
                carpool.delete()
                return JsonResponse({'status': 204}, status=204)
            else:
                return JsonResponse({'status': 404, 'detail': 'This carpool does not exist.'}, status=404)
