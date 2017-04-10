import hmac
import json
import os
from datetime import datetime

from django.conf import settings
from django.core import serializers
from django.http import JsonResponse, QueryDict
from django.utils import timezone
from django.views.generic.base import View
from passlib.hash import pbkdf2_sha256 as hasher

from .forms import UserForm, CarpoolForm, AuthenticatorForm
from .models import User, Carpool, Authenticator


def as_dict(body):
    """
    :param body: QueryDict, dict, str
    :return: dict
    """
    if isinstance(body, QueryDict):  # request.POST body
        return body.dict()
    elif isinstance(body, str):  # x-www-form-urlencoded body
        return QueryDict(body).dict()
    else:  # already a dict
        return body


def as_json(data):
    if isinstance(data, dict) or isinstance(data, QueryDict):
        return json.dumps(data)
    else:
        return data


def success_response(status_code, detail, auth_token=None, data=None):
    assert (isinstance(detail, dict) or isinstance(detail, str)) and (auth_token is None or len(auth_token) == 64)
    response = {'detail': str(detail), 'auth_token': auth_token}
    if data:
        response['data'] = as_json(data)
    return JsonResponse(response, status=status_code)


def failure_response(status_code, detail, auth_token=None):
    assert (isinstance(detail, dict) or isinstance(detail, str)) and (auth_token is None or len(auth_token) == 64)
    response = {'detail': str(detail), 'auth_token': auth_token}
    return JsonResponse(response, status=status_code)


def index(request):
    if request.method == 'GET':
        return success_response(status_code=200, detail='This is the model API entry point.')


def get_authenticator(authenticator=None, username=None):
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


def update_user(body, instance=None):
    """
    Make sure you use the same salt when you store the password as when you're checking it
    :param body:
    :param instance:
    :return:
    """
    body = as_dict(body)
    body['password'] = hasher.hash(body['password'])
    form = UserForm(body, instance=instance)
    if form.is_valid():
        user = form.save()
        if user.carpool_joined:
            carpool = get_carpool(pk=user.carpool_joined.pk)
            if not carpool:
                return failure_response(status_code=404, detail='This carpool does not exist.')
            carpool.passengers.add(user)
            assert user.pk in carpool.passengers
            carpool.save()
        data = json.loads(serializers.serialize('json', [user, ]))
        return success_response(status_code=201, detail='User {} is successfully updated.'.format(user.username),
                                data=data)
    else:
        return failure_response(status_code=400, detail=dict(form.errors.items()))


def update_carpool(form):
    if form.is_valid():
        carpool = form.save()
        user = get_user(pk=carpool.driver.pk)
        if not user:
            return failure_response(status_code=404, detail='This usuer does not exist.')
        user.carpool_owned = carpool
        if carpool.passengers:
            for user_pk in carpool.passengers.all():
                User.objects.filter(pk=user_pk).update(carpool_joined=carpool.pk)
        user.save()
        data = json.loads(serializers.serialize('json', [carpool, ]))
        return success_response(status_code=201, detail='Carpool {} is successfully updated.'.format(carpool.pk),
                                data=data)
    else:
        return failure_response(status_code=400, detail=dict(form.errors.items()))


class UserList(View):
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


class UserDetail(View):
    def get(self, request, pk=None, username=None):
        """
        :param request:
        :param pk:
        :param username:
        :return:
        """
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

    def put(self, request, pk=None):
        """
        :param request:
        :param pk:
        :param username:
        :return:
        """
        if request.method == 'PUT':
            user = None
            if pk:
                user = get_user(pk=pk)
            if user:
                body = QueryDict(request.body.decode('utf-8'))
                return update_user(body=body, instance=user)
            else:
                return failure_response(status_code=404, detail='This user does not exist.')

    def delete(self, request, pk=None, username=None):
        """
        :param request:
        :param pk:
        :param username:
        :return:
        """
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


class Authentication(View):
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
        authenticator = None
        if username:
            authenticator = get_authenticator(username=username)
        if auth_token:
            authenticator = get_authenticator(auth_token=auth_token)
        response = {}
        if authenticator:
            time_delta = (timezone.now() - authenticator.date_created).days * 24 * 60
            if time_delta <= 60:  # token cannot be longer than an hour
                response['auth'] = authenticator.authenticator
                response['status'] = 200
                response['detail'] = 'Authenticator is valid.'
                return JsonResponse(response, status=200)
            else:
                authenticator.delete()
                response['auth'] = None
                response['status'] = 404
                response['detail'] = 'Authenticator expired.'
                return JsonResponse(response, status=404)
        else:
            return JsonResponse({'status': 404, 'detail': 'This authenticator does not exist.'},
                                status=404)

    def post(self, request):
        """
        POST /v1/auth/
        Call only when user logs in
        Validate user login info in exp layer, not model layer
        :param request: username, password
        :return:
        """
        try:
            assert 'username' in request.POST and 'password' in request.POST
        except AssertionError:
            return failure_response(status_code=400,
                                    detail='Username or password is missing.')
        user = get_user(username=request.POST['username'])
        if not user:
            return failure_response(status_code=400, detail='User {} does not exist.'.format(request.POST['username']))
        authenticator = get_authenticator(username=request.POST['username'])
        if authenticator:
            return failure_response(status_code=409, detail='User {} is already authenticated.'.format(
                request.POST['username']), auth_token=authenticator.authenticator)
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

    def delete(self, request, username=None, authenticator=None):
        """
        DELETE /v1/auth/{username}/
        DELETE /v1/auth/{auth_token}/
        Call only when user logs out
        :param request:
        :param username:
        :param authenticator:
        :return:
        """
        if request.method == 'DELETE':
            token = None
            if username:
                token = get_authenticator(username=username)
            if authenticator:
                token = get_authenticator(authenticator=authenticator)
            if token:
                token.delete()
                return JsonResponse({'status': 204}, status=204)
            else:
                return JsonResponse({'status': 404, 'detail': 'This authenticator does not exist.'},
                                    status=404)


class CarpoolList(View):
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


class CarpoolDetail(View):
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
                form = CarpoolForm(request.PUT, instance=carpool)
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
