import json

import requests
from django.http import JsonResponse
from elasticsearch import Elasticsearch
from kafka import KafkaProducer
from rest_framework.views import APIView

from .forms import UserLoginForm, UserRegistrationForm, CarpoolListingForm

MODEL_API = 'http://model-api:8000/v1/'  # in docker VM, but in root computer, it's localhost:8001/v1/
producer = KafkaProducer(bootstrap_servers='kafka:9092')


def index(request):
    if request.method == 'GET':
        return JsonResponse({'detail': 'This is the experience API entry point.'}, status=200)


def success_response(response):
    pass


def failure_response(response):
    pass


def search(request):
    query = request.POST['query']
    es = Elasticsearch([{'host': 'es', 'port': 9200}])
    results = es.search(index='carpool_index', body={'query': {'query_string': {'query': query}}, 'size': 10})
    return JsonResponse(results)


class UserRegistration(APIView):
    def post(self, request):
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                response = requests.post(MODEL_API + 'users/', data=form.cleaned_data)
                response_json = response.json()
                return JsonResponse(response_json, status=response.status_code)
            else:
                return JsonResponse({'detail': form.errors}, status=400)


class UserLogin(APIView):
    def post(self, request):
        if request.method == 'POST':
            form = UserLoginForm(request.POST)
            if form.is_valid():
                response = requests.post(MODEL_API + 'auth/', data=form.cleaned_data)
                response_json = response.json()
                return JsonResponse(response_json, status=response.status_code)
            else:
                return JsonResponse({'detail': form.errors}, status=400)


class UserLogout(APIView):
    def delete(self, request, auth_token):
        if request.method == 'DELETE':
            # auth_token = request.data['auth_token']
            response = requests.delete(MODEL_API + 'auth/' + auth_token + '/')
            return JsonResponse({'detail': 'Deleted logout'}, status=204)


class UserDetail(APIView):
    def get(self, request, pk=None, username=None):
        if request.method == 'GET':
            response = None
            if pk:
                response = requests.get(MODEL_API + 'users/' + pk + '/')
            elif username:
                response = requests.get(MODEL_API + 'users/' + username + '/')
            response_json = response.json()
            return JsonResponse(response_json, status=response.status_code)


class UsersFilter(APIView):
    def get(self, request):
        if request.method == 'GET':
            response = requests.get(MODEL_API + 'users/').json()
            return JsonResponse(response)


class CarpoolDetail(APIView):
    def get(self, request, pk):
        if request.method == 'GET':
            response = requests.get(MODEL_API + 'carpools/' + pk).json()
            return JsonResponse(response)


class CarpoolsFilter(APIView):
    def get(self, request):
        if request.method == 'GET':
            data = {}
            carpools_response = requests.get(MODEL_API + 'carpools/').json()
            users_response = requests.get(MODEL_API + 'users/').json()
            if carpools_response and users_response:
                data['carpools'] = carpools_response['data']
                data['users'] = users_response['data']
                return JsonResponse(data, safe=False)

    def post(self, request):
        if request.method == 'POST':
            form = CarpoolListingForm(request.POST)
            if form.is_valid():
                response = requests.post(MODEL_API + 'carpools/', data=form.cleaned_data)
                response_json = response.json()
                producer.send('new_carpools_topic', json.dumps(response_json).encode('utf-8'))
                return JsonResponse(response_json, status=response.status_code)
            else:
                return JsonResponse({'detail': form.errors}, status=400)
