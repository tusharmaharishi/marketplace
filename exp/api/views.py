import json

import requests
from django.http import JsonResponse, QueryDict
from elasticsearch import Elasticsearch
from kafka import KafkaProducer
from requests.compat import urljoin

from .forms import UserLoginForm, UserRegistrationForm, CarpoolListingForm

MODEL_API = 'http://model-api:8000/v1/'  # in docker VM, but in root computer, it's localhost:8001/v1/
producer = KafkaProducer(bootstrap_servers='kafka:9092', retries=5)


def index(request):
    if request.method == 'GET':
        return JsonResponse({'detail': 'This is the experience API entry point.'}, status=200)


def success_response(status_code, detail='', auth_token=None, data=None):
    if auth_token and len(auth_token) != 64:
        return JsonResponse({'detail': 'This authenticator is not valid.'}, status=400)
    res = {'detail': str(detail), 'auth_token': auth_token}
    if data:
        if isinstance(data, dict) or isinstance(data, QueryDict) or isinstance(data, list):
            response['data'] = data
        else:
            try:
                response['data'] = json.loads(data)
            except ValueError:
                return JsonResponse({'detail': 'This data is not valid.'}, status=400)
    return JsonResponse(response, status=status_code)


def failure_response(status_code, detail='', auth_token=None):
    if auth_token and len(auth_token) != 64:
        return JsonResponse({'detail': 'This authenticator is not valid.'}, status=400)
    res = {'detail': str(detail), 'auth_token': auth_token}
    return JsonResponse(response, status=status_code)


def www_urlencoded_to_dict(body):
    """
    Converts raw x-www-form-urlencoded request data to mutable dict
    This QueryDict instance is immutable error, must QueryDict.copy()
    :param body:
    :return: QueryDict or None
    """
    body = body.decode('utf-8')
    data = QueryDict(body).copy()
    return data


def create_user(request):
    if request.method == 'POST':
        body = www_urlencoded_to_dict(request.body)
        form = UserRegistrationForm(body)
        if form.is_valid():
            try:
                res = requests.post(urljoin(MODEL_API, 'users/'), data=form.cleaned_data)
            except requests.exceptions.RequestException as e:
                return failure_response(status_code=400, detail=e.message)
            res_json = res.json()
            if res.status_code // 100 == 2:
                return success_response(status_code=res.status_code, detail=res_json['detail'], data=res_json['data'])
            else:
                return failure_response(status_code=res.status_code, detail=res_json['detail'])
        else:
            return failure_response(status_code=400, detail=str(dict(form.errors.items())))


def create_authenticator(request):  # login
    if request.method == 'POST':
        body = www_urlencoded_to_dict(request.body)
        form = UserLoginForm(body)
        if form.is_valid():
            try:
                res = requests.post(urljoin(MODEL_API, 'auth/'), data=form.cleaned_data)
            except requests.exceptions.RequestException as e:
                return failure_response(status_code=400, detail=e.message)
            res_json = res.json()
            if res.status_code // 100 == 2:
                return success_response(status_code=res.status_code, detail=res_json['detail'],
                                        auth_token=res_json['auth_token'])
            else:
                return failure_response(status_code=res.status_code, detail=res_json['detail'])
        else:
            return failure_response(status_code=400, detail=str(dict(form.errors.items())))


def delete_authenticator(request, username):  # logout
    if request.method == 'DELETE':
        try:
            res = requests.delete(urljoin(MODEL_API, 'auth', username))
        except requests.exceptions.RequestException as e:
            return failure_response(status_code=400, detail=e.message)
        res_json = res.json()
        if res.status_code // 100 == 2:
            return success_response(status_code=res.status_code)
        else:
            return failure_response(status_code=res.status_code, detail=res_json['detail'])


def create_carpool(request):
    if request.method == 'POST':
        body = www_urlencoded_to_dict(request.body)
        form = CarpoolListingForm(body)
        if form.is_valid():
            data = form.cleaned_data.copy()
            data['auth_token'] = body.get('auth_token')  # return None if no auth_token
            try:
                res = requests.post(urljoin(MODEL_API, 'carpools/'), data=data)
            except requests.exceptions.RequestException as e:
                return failure_response(status_code=400, detail=e.message)
            res_json = res.json()
            if res.status_code // 100 == 2:
                producer.send('new-listings-topic', json.dumps(res_json).encode('utf-8'))
                return success_response(status_code=res.status_code, detail=res_json['detail'], data=res_json['data'],
                                        auth_token=res_json['auth_token'])
            else:
                return failure_response(status_code=res.status_code, detail=res_json['detail'],
                                        auth_token=res_json['auth_token'])
        else:
            return failure_response(status_code=400, detail=str(dict(form.errors.items())))


def get_driver_by_carpool(request):
    if request.method == 'GET':
        if 'carpool_pk' in request.GET:
            params = {'auth_token': request.GET.get('auth_token')}
            try:
                carpool_res = requests.get(urljoin(MODEL_API, 'carpools', request.GET['carpool_pk']), params=params)
            except requests.exceptions.RequestException as e:
                return failure_response(status_code=400, detail=e.message)
            carpool_res_json = carpool_res.json()
            if carpool_res.status_code // 100 == 2:
                carpool = carpool_res_json['data']['carpools'][0]  # only one carpool json object in data
                params['carpool_owned'] = carpool['pk']
                try:
                    driver_res = requests.get(urljoin(MODEL_API, 'users'), params=params)
                except requests.exceptions.RequestException as e:
                    return failure_response(status_code=400, detail=e.message)
                driver_res_json = driver_res.json()
                if driver_res.status_code // 100 == 2:
                    driver = driver_res_json['data']['users'][0]
                    return success_response(status_code=driver_res.status_code, data=driver,
                                            auth_token=driver_res_json['auth_token'])
                else:
                    return failure_response(status_code=driver_res.status_code, detail=driver_res_json['detail'],
                                            auth_token=driver_res_json['auth_token'])
            else:
                return failure_response(status_code=carpool_res.status_code, detail=carpool_res_json['detail'],
                                        auth_token=carpool_res_json['auth_token'])
        else:
            return failure_response(status_code=400, detail='This request is missing required fields.')


def get_passengers_by_carpool(request):
    if request.method == 'GET':
        if 'carpool_pk' in request.GET:
            params = {'auth_token': request.GET.get('auth_token')}
            try:
                carpool_res = requests.get(urljoin(MODEL_API, 'carpools', request.GET['carpool_pk']), params=params)
            except requests.exceptions.RequestException as e:
                return failure_response(status_code=400, detail=e.message)
            carpool_res_json = carpool_res.json()
            if carpool_res.status_code // 100 == 2:
                carpool = carpool_res_json['data']['carpools'][0]  # only one carpool json object in data
                params['carpool_joined'] = carpool['pk']
                try:
                    passengers_res = driver_res = requests.get(urljoin(MODEL_API, 'users'), params=params)
                except requests.exceptions.RequestException as e:
                    return failure_response(status_code=400, detail=e.message)
                passengers_res_json = passengers_res.json()
                if passengers_res.status_code // 100 == 2:
                    passengers = passengers_res_json['data']['users']
                    return success_response(status_code=passengers_res.status_code, data=passengers,
                                            auth_token=passengers_res_json['auth_token'])
                else:
                    return failure_response(status_code=passengers_res.status_code,
                                            detail=passengers_res_json['detail'],
                                            auth_token=passengers_res_json['auth_token'])
            else:
                return failure_response(status_code=carpool_res.status_code, detail=carpool_res_json['detail'],
                                        auth_token=carpool_res_json['auth_token'])
        else:
            return failure_response(status_code=400, detail='This request is missing required fields.')


def get_carpools_by_driver(request):
    if request.method == 'GET':
        res = requests.get(MODEL_API + 'carpools/' + pk).json()
        return JsonResponse(res)


def get_carpools_by_passenger(request):
    pass


def get_carpools_by_location(request):
    if request.method == 'GET':
        data = {}
        carpools_res = requests.get(MODEL_API + 'carpools/').json()
        users_res = requests.get(MODEL_API + 'users/').json()
        if carpools_res and users_response:
            data['carpools'] = carpools_response['data']
            data['users'] = users_response['data']
            return JsonResponse(data, safe=False)


def search_carpools(request):
    print('SEARCH')
    if request.method == 'POST':
        keywords = request.GET['keywords']
        es = Elasticsearch([{'host': 'es', 'port': 9200}])
        results = es.search(index='listing_index', body={'query': {'query_string': {'query': keywords}}, 'size': 10})
        print('RESULTS', results)
        return JsonResponse(results)
