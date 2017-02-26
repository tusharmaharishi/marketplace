from django.shortcuts import render
import urllib.request
import urllib.parse
import json
import requests

BASE_API = 'http://model-api:8000/v1/'

def list_users(request):
    # res = requests.get(BASE_API + 'users/')
    # return render(request, 'list_user.html', {'user_list': res})
    req = urllib.request.Request(BASE_API + 'users/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    res = json.loads(resp_json)
    return render(request, 'list_user.html', {'user_list': res}, content_type='application/json')