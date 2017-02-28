from django.shortcuts import render
import urllib.request
import urllib.parse
import json
import requests

BASE_API = 'http://exp-api:8000/v1/'

def list_users(request):
    res = requests.get(BASE_API + 'users/')
    return render(request, 'list_user.html', {'user_list': res.json()})