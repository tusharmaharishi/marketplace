import requests
from django.shortcuts import render

BASE_API = 'http://exp-api:8000/'


def get_home_page(request):
    response = requests.get(BASE_API + 'v1/latest/').json()
    data = response['carpools']
    return render(request, 'index.html', {'latest_rides': data})


def get_users(request):
    response = requests.get(BASE_API + 'v1/users/').json()
    data = response['data']
    return render(request, 'list_user.html', {'user_list': data})


def get_user_detail(request, pk):
    response = requests.get(BASE_API + 'v1/users/' + pk + '/')
    try:
        data = response.json()['data']
        return render(request, 'list_user.html', {'user_list': data})
    except:
        return render(request, 'list_user.html')
