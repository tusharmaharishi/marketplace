import requests
from django.shortcuts import render

BASE_API = 'http://model-api:8000/v1/'


def get_home_page(request):
    carpools = requests.get(BASE_API + 'carpools/').json()
    data = carpools['data']
    return render(request, 'index.html', {'latest_rides': data})


def get_users(request):
    res = requests.get(BASE_API + 'users/').json()
    data = res['data']
    return render(request, 'list_user.html', {'user_list': data})


def get_user_detail(request, pk):
    res = requests.get(BASE_API + 'users/' + pk + '/').json()
    data = res['data']
    return render(request, 'list_user.html', {'user_list': data})
