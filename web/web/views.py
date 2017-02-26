from django.shortcuts import render
import urllib.request
import urllib.parse
import requests
import json

BASE_API = 'http://model-api:8000/v1/'

def list_users(request):
    res = requests.get(BASE_API + 'users/')
    print(res.json())