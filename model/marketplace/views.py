import hmac
import json
import os
from datetime import datetime

from django.conf import settings
from django.core import serializers
from django.http import JsonResponse, QueryDict
from django.views.generic.base import View
from passlib.hash import pbkdf2_sha256 as hasher

from .forms import UserForm, CarpoolForm, AuthenticatorForm
from .models import User, Carpool, Authenticator


def success_response(status_code, detail='', auth_token=None, data=None):
    assert isinstance(detail, str) and (auth_token is None or len(auth_token) == 64)
    response = {'detail': str(detail), 'auth_token': auth_token}
    if data:
        if isinstance(data, dict) or isinstance(data, QueryDict):
            response['data'] = json.dumps(data)
        else:
            response['data'] = data
    return JsonResponse(response, status=status_code)


def failure_response(status_code, detail='', auth_token=None):
    assert isinstance(detail, str) and (auth_token is None or len(auth_token) == 64)
    response = {'detail': str(detail), 'auth_token': auth_token}
    return JsonResponse(response, status=status_code)


def get_authenticator(auth_token=None, username=None):
    if auth_token:
        try:
            return Authenticator.objects.get(auth_token=auth_token)
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


def update_user(body, instance=None):
    """
    Make sure you use the same salt when you store the password as when you're checking it
    :param body:
    :param instance:
    :return:
    """
    if not isinstance(body, QueryDict) or not isinstance(body, dict):
        return failure_response(status_code=400)
    form = UserForm(body, instance=instance)
    if form.is_valid():
        user = form.save()
        if user.carpool_joined:
            carpool = get_carpool(pk=user.carpool_joined.pk)
            if not carpool:
                return failure_response(status_code=404, detail='This carpool does not exist.')
            carpool.passengers.add(user)
            carpool.save()
        data = json.loads(serializers.serialize('json', [user, ]))
        return success_response(status_code=201, detail='This user has been successfully updated.', data=data)
    else:
        return failure_response(status_code=400, detail=str(dict(form.errors.items())))


def update_carpool(body, instance=None):
    if not isinstance(body, QueryDict) or not isinstance(body, dict) or 'auth_token' not in body:
        return failure_response(status_code=400)
    form = CarpoolForm(body, instance=instance)
    if form.is_valid():
        carpool = form.save()
        user = get_user(pk=carpool.driver.pk)
        if not user:
            return failure_response(status_code=404, detail='This user does not exist.')
        user.carpool_owned = carpool
        if carpool.passengers:
            for user_pk in carpool.passengers.all():
                User.objects.filter(pk=user_pk).update(carpool_joined=carpool.pk)
        user.save()
        data = json.loads(serializers.serialize('json', [carpool, ]))
        return success_response(status_code=201, detail='This carpool has been successfully updated.', data=data,
                                auth_token=body['auth_token'])
    else:
        return failure_response(status_code=400, detail=str(dict(form.errors.items())), auth_token=body['auth_token'])


def index(request):
    if request.method == 'GET':
        return success_response(status_code=200, detail='This is the model API entry point.')


class UserView(View):
    def get(self, request, pk=None, username=None):
        """
        GET /v1/users
        GET /v1/users/{pk}
        GET /v1/users/{username}
        :param request:
        :param pk:
        :param username:
        :return:
        """
        if request.method == 'GET':
            if pk or username:
                user = get_user(pk=pk) if pk else get_user(username=username)
                if user:
                    data = json.loads(serializers.serialize('json', [user, ]))
                    return success_response(status_code=200, data=data)
                else:
                    return failure_response(status_code=404, detail='This user does not exist.')
            else:
                users = User.objects.all()
                if users:
                    data = json.loads(serializers.serialize('json', users))
                    data['count'] = users.count()
                    return success_response(status_code=200, data=data)
                else:
                    return failure_response(status_code=404, detail='These users do not exist.')

    def post(self, request):
        """
        POST /v1/users
        :param request:
        :return:
        """
        if request.method == 'POST':
            body = request.body.decode('utf-8')
            body = QueryDict(body)
            if 'username' in body and 'password' in body:
                if User.objects.filter(username=body['username']).exists():
                    return failure_response(status_code=409, detail='This username already exists.')
                body['password'] = hasher.hash(body['password'])
                return update_user(body=body)
            else:
                return failure_response(status_code=400, detail='This request is missing required fields.')

    def put(self, request, pk=None, username=None):
        """
        PUT /v1/users/{pk}
        PUT /v1/users/{username}
        :param request:
        :param pk:
        :param username:
        :return:
        """
        if request.method == 'PUT':
            body = request.body.decode('utf-8')
            body = QueryDict(body)
            user = None
            if 'username' in body and 'password' in body:
                if User.objects.filter(username=body['username']).exists():
                    return failure_response(status_code=409, detail='This username already exists.')
                if pk:
                    user = get_user(pk=pk)
                elif username:
                    user = get_user(username=username)
            if user:
                body['password'] = hasher.hash(body['password'])
                return update_user(body=body, instance=user)
            else:
                return failure_response(status_code=400, detail='This request is missing required fields.')

    def delete(self, request, pk=None, username=None):
        """
        DELETE /v1/users/{pk}
        DELETE /v1/users/{username}
        :param request:
        :param pk:
        :param username:
        :return:
        """
        if request.method == 'DELETE':
            if pk or username:
                user = get_user(pk=pk) if pk else get_user(username=username)
                if user:
                    user.delete()
                    return success_response(status_code=204, detail='This user has been deleted.')
                else:
                    return failure_response(status_code=404, detail='This user does not exist.')
            else:
                User.objects.all().delete()
                return success_response(status_code=204, detail='These users have been deleted.')


class CarpoolView(View):
    def get(self, request, pk=None):
        """
        GET /v1/carpools
        GET /v1/carpools/{pk}
        GET /v1/carpools?driver=&driver_username=&passenger=&passenger_username=&location_start=&location_end=
        :param request:
        :param pk:
        :return:
        """
        if request.method == 'GET':
            if 'auth_token' not in request.GET:
                return failure_response(status_code=401, detail='This user is not logged in to perform this request.')
            auth_token = request.GET['auth_token']
            if pk:
                carpool = get_carpool(pk=pk)
                if carpool:
                    data = json.loads(serializers.serialize('json', [carpool, ]))
                    return success_response(status_code=200, auth_token=auth_token, data=data)
                else:
                    return failure_response(status_code=404, auth_token=auth_token,
                                            detail='This carpool does not exist.')
            else:
                carpools = None
                if request.GET.get('driver'):  # get carpool by driver id
                    if not isinstance(request.GET.get('driver'), int):
                        return failure_response(status_code=400, detail='This driver does not exist.',
                                                auth_token=auth_token)
                    carpools = Carpool.objects.filter(driver=request.GET.get('driver'))
                elif request.GET.get('driver_username'):  # get carpool by driver username
                    if not isinstance(request.GET.get('driver_username'), str):
                        return failure_response(status_code=400, detail='This driver does not exist.',
                                                auth_token=auth_token)
                    driver = get_user(username=request.GET.get('driver_username'))
                    carpools = Carpool.objects.filter(driver=driver.pk)
                elif request.GET.get('passenger'):
                    if not isinstance(request.GET.get('passenger'), int):
                        return failure_response(status_code=400, detail='This passenger does not exist.',
                                                auth_token=auth_token)
                    carpools = Carpool.objects.filter(passengers__in=[request.GET.get('passenger')])
                elif request.GET.get('passenger_username'):
                    if not isinstance(request.GET.get('passenger_username'), str):
                        return failure_response(status_code=400, detail='This passenger does not exist.',
                                                auth_token=auth_token)
                    passenger = get_user(username=request.GET.get('passenger_username'))
                    carpools = Carpool.objects.filter(passengers__in=[passenger.pk])
                elif (request.GET.get('location_start_lat') and request.GET.get('location_start_lon')) and (
                            request.GET.get('location_end_lat') and request.GET.get('location_end_lon')):
                    location_start_lat = request.GET.get('location_start_lat')
                    location_start_lon = request.GET.get('location_start_lon')
                    location_end_lat = request.GET.get('location_end_lat')
                    location_end_lon = request.GET.get('location_end_lon')
                    if isinstance(location_start_lat, float) and isinstance(location_start_lon, float) and isinstance(
                            location_end_lat, float) and isinstance(location_end_lon, float):
                        carpools = Carpool.objects.filter(
                            location_start_lat__range=(location_start_lat - 0.5, location_start_lat + 0.5),
                            location_start_lon__range=(location_start_lon - 0.5, location_start_lon + 0.5),
                            location_end_lat__range=(location_end_lat - 0.5, location_end_lat + 0.5),
                            location_end_lon__range=(location_end_lon - 0.5, location_end_lon + 0.5))
                    else:
                        return failure_response(status_code=400, detail='These locations do not exist.',
                                                auth_token=auth_token)
                elif not request.GET.keys():
                    carpools = Carpool.objects.all()
                if carpools:
                    data = json.loads(serializers.serialize('json', carpools))
                    data['count'] = carpools.count()
                    return success_response(status_code=200, auth_token=auth_token, data=data)
                else:
                    return failure_response(status_code=404, auth_token=auth_token,
                                            detail='These carpools do not exist.')

    def post(self, request):
        """
        POST /v1/carpools
        :param request:
        :return:
        """
        if request.method == 'POST':
            body = request.body.decode('utf-8')
            body = QueryDict(body)
            if 'auth_token' not in body:
                return failure_response(status_code=401, detail='This user is not logged in to perform this request.')
            return update_carpool(body=body)

    def put(self, request, pk):
        """
        PUT /v1/carpools/{pk}
        :param request:
        :param pk:
        :return:
        """
        if request.method == 'PUT':
            body = request.body.decode('utf-8')
            body = QueryDict(body)
            if 'auth_token' not in body:
                return failure_response(status_code=401, detail='This user is not logged in to perform this request.')
            auth_token = body['auth_token']
            carpool = get_carpool(pk=pk)
            if carpool:
                return update_carpool(body=body, instance=carpool)
            else:
                return failure_response(status_code=404, detail='This carpool does not exist.', auth_token=auth_token)

    def delete(self, request, pk=None):
        if request.method == 'DELETE':
            body = request.body.decode('utf-8')
            body = QueryDict(body)
            if 'auth_token' not in body:
                return failure_response(status_code=401, detail='This user is not logged in to perform this request.')
            auth_token = body['auth_token']
            if pk:
                carpool = get_carpool(pk=pk)
                if carpool:
                    carpool.delete()
                    return success_response(status_code=204, detail='This carpool has been deleted.',
                                            auth_token=auth_token)
                else:
                    return failure_response(status_code=404, detail='This carpool does not exist.',
                                            auth_token=auth_token)
            else:
                Carpool.objects.all().delete()
                return success_response(status_code=204, detail='These carpools have been deleted.')


class AuthenticationView(View):
    def get(self, request, username=None, auth_token=None):
        """
        GET /v1/auth/{username}/
        GET /v1/auth/{auth_token}/
        Call every time user does something while logged in
        :param request:
        :param username:
        :param auth_token:
        :return:
        """
        if request.method == 'GET':
            authenticator = None
            if username:
                authenticator = get_authenticator(username=username)
            if auth_token:
                authenticator = get_authenticator(auth_token=auth_token)
            if authenticator:
                return success_response(status_code=200, detail='This authenticator is valid.',
                                        auth_token=authenticator.auth_token)
            else:
                return failure_response(status_code=404, detail='This authenticator does not exist.')

    def post(self, request):
        """
        POST /v1/auth/
        Call only when user logs in
        Validate user login info in exp layer, not model layer
        :param request: username, password
        :return:
        """
        if request.method == 'POST':
            try:
                assert 'username' in request.POST and 'password' in request.POST
            except AssertionError:
                return failure_response(status_code=400,
                                        detail='This user is missing username or password.')
            user = get_user(username=request.POST['username'])
            if not user:
                return failure_response(status_code=400, detail='This user does not exist.')
            authenticator = get_authenticator(username=request.POST['username'])
            if authenticator:
                return failure_response(status_code=409, detail='User {} is already authenticated.'.format(
                    request.POST['username']), auth_token=authenticator.auth_token)
            elif hasher.verify(request.POST['password'], user.password):
                auth_token = hmac.new(
                    key=settings.SECRET_KEY.encode('utf-8'),
                    msg=os.urandom(32),
                    digestmod='sha256',
                ).hexdigest()
                if Authenticator.objects.filter(auth_token=auth_token).exists():
                    return failure_response(status_code=409, detail='This auth_token already exists for another user.')
                auth = AuthenticatorForm({'username': request.POST['username'],
                                          'auth_token': auth_token,
                                          'date_created': datetime.now()})
                auth.save()
                return success_response(status_code=201,
                                        detail='Authenticator is successfully created for user {}.'.format(
                                            request.POST['username']), auth_token=auth_token)
            else:
                return failure_response(status_code=400,
                                        detail='Passwords for user {} do not match.'.format(request.POST['username']))

    def delete(self, request, username=None, auth_token=None):
        """
        DELETE /v1/auth/{username}/
        DELETE /v1/auth/{auth_token}/
        Call only when user logs out
        :param request:
        :param username:
        :param auth_token:
        :return:
        """
        if request.method == 'DELETE':
            authenticator = None
            if username:
                authenticator = get_authenticator(username=username)
            if authenticator:
                authenticator = get_authenticator(auth_token=auth_token)
            if authenticator:
                authenticator.delete()
                return success_response(status_code=204, detail='This authenticator is successfully deleted.')
            else:
                return failure_response(status_code=404, detail='This authenticator does not exist.')
