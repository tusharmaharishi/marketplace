import json

import requests
from django.http import JsonResponse
from .forms import UserLoginForm

MODEL_API = 'http://model-api:8000/v1/'


def index(request):
    if request.method == 'GET':
        return JsonResponse({'status': 200, 'message': 'This is the experience API entry point.'}, status=200)


def register_new_user(request):
    if request.method == 'POST':
        response = requests.post(MODEL_API + 'users/', data=json.dumps(request.POST))
        return response


def login_user(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        form = UserLoginForm(data)
        if form.is_valid():
            print('in exp {}'.format(form.cleaned_data))
            username, password = form.cleaned_data['username'], form.cleaned_data['password']
            # print('user: ', username, 'pass: ', password)
            response = requests.post(MODEL_API + 'auth/', data=json.dumps(form.cleaned_data)).json()
            print(response)
            return JsonResponse(response)
        else:
            return JsonResponse({'status': 404, 'detail': 'login not working'})


def logout_user(request):
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
