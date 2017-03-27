import json

import requests
from django.http import JsonResponse
from rest_framework.views import APIView

from .forms import UserLoginForm

MODEL_API = 'http://model-api:8000/v1/'  # in docker VM, but in root computer, it's localhost:8001/v1/


def index(request):
    if request.method == 'GET':
        return JsonResponse({'status': 200, 'message': 'This is the experience API entry point.'}, status=200)


class UserRegistration(APIView):
    def post(self, request):
        if request.method == 'POST':
            response = requests.post(MODEL_API + 'users/', data=json.dumps(request.POST))
            return response


class UserLogin(APIView):
    def post(self, request):
        if request.method == 'POST':
            print('in exp post {}'.format(json.dumps(request.POST)))
            form = UserLoginForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['username'] and form.cleaned_data['password']:
                    print(json.dumps(form.cleaned_data))
                    response = requests.post(MODEL_API + 'auth/', data=json.dumps(form.cleaned_data)).json()
                    return JsonResponse(response)
                else:
                    return JsonResponse({'status': 400, 'detail': 'Login request is missing username and/or password.'})
            else:
                return JsonResponse({'status': 404, 'detail': 'User login form is not valid.'})


class UserLogout(APIView):
    def post(self, request):
        if request.method == 'POST':
            # authenticator = request.data['authenticator']
            response = requests.delete(MODEL_API + 'auth/' + request.POST['username'])
            return response


def get_user_detail(request, pk):
    if request.method == 'GET':
        response = requests.get(MODEL_API + 'users/' + pk + '/').json()
        if response['status'] == 200:
            return JsonResponse(response)
        else:
            return response['message']


def get_users(request):
    if request.method == 'GET':
        response = requests.get(MODEL_API + 'users/').json()
        return JsonResponse(response)


def get_latest_data(request):
    if request.method == 'GET':
        data = {}
        carpools_response = requests.get(MODEL_API + 'carpools/').json()
        users_response = requests.get(MODEL_API + 'users/').json()
        if carpools_response and users_response:
            data['carpools'] = carpools_response['data']
            data['users'] = users_response['data']
            return JsonResponse(data, safe=False, status=200)
