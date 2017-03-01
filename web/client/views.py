import requests
from django.shortcuts import render

BASE_API = 'http://model-api:8000/v1/'


def index(request):
    return render(request, 'index.html')


def list_users(request):
    res = requests.get(BASE_API + 'users/2/').json()
    data = res['data']
    return render(request, 'list_user.html', {'user_list': data})
