import json

import requests
from django.http import JsonResponse
from rest_framework.views import APIView

from .forms import UserLoginForm, UserRegistrationForm, CarpoolListingForm

MODEL_API = 'http://model-api:8000/v1/'  # in docker VM, but in root computer, it's localhost:8001/v1/


def index(request):
    if request.method == 'GET':
        return JsonResponse({'detail': 'This is the experience API entry point.'}, status=200)


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
    def delete(self, request, authenticator):
        if request.method == 'DELETE':
            # authenticator = request.data['authenticator']
            response = requests.delete(MODEL_API + 'auth/' + authenticator + '/')
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
                print(response_json)
                return JsonResponse(response_json, status=response.status_code)
            else:
                return JsonResponse({'detail': form.errors}, status=400)
