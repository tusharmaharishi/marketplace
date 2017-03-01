import requests
from django.shortcuts import render

BASE_API = 'http://model-api:8000/v1/'


def index(request):
	carpools = requests.get(BASE_API  + 'carpools/').json()
	data = carpools['data']
	return render(request, 'index.html', {'latest_rides': data})


def list_users(request):
    res = requests.get(BASE_API + 'users/2/').json()
    data = res['data']
    return render(request, 'list_user.html', {'user_list': data})

def user_detail(request):
	res = requests.get(BASE_API + 'users/1/').json()
	data = res['data']
	return render(request, 'list_user.html', {'user_list': data})
