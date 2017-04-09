import json

import requests
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import UserLoginForm, UserRegistrationForm, CreateCarpoolForm, SearchForm

BASE_API = 'http://exp-api:8000/v1/'  # in docker VM, but in root computer, it's localhost:8002/v1/


def get_home_page(request):
    response = requests.get(BASE_API + 'carpools/').json()
    carpools = response['carpools']
    users = response['users']
    return render(request, 'index.html', {'latest_rides': carpools, 'latest_drivers': users})


def get_users(request):
    response = requests.get(BASE_API + 'users/').json()
    data = response['data']
    return render(request, 'list_user.html', {'user_list': data})


def get_user_detail(request, pk):
    response = requests.get(BASE_API + 'users/' + pk + '/')
    try:
        data = response.json()['data']
        return render(request, 'list_user.html', {'user_list': data})
    except:
        return render(request, 'list_user.html')


def get_carpools(request):
    response = requests.get(BASE_API + 'carpools/').json()
    data = response['carpools']
    return render(request, 'list_carpools.html', {'carpool_list': data})


def get_carpool_detail(request, pk):
    response = requests.get(BASE_API + 'carpools/' + pk + '/').json()
    try:
        data = response.json()['data']
        return render(request, 'list_carpools.html', {'carpool_list': data})
    except:
        return render(request, 'list_carpools.html')




# def login_required(f):
#     def wrap(request, *args, **kwargs):
#         next_url = reverse('index')
#         response = HttpResponseRedirect(next_url)
#         auth = request.COOKIES.get('auth')
#         if auth:
#             response = requests.get(BASE_API + '/auth/' + str(auth)).json()
#             if response['status'] == 200:
#                 return f(request, *args, **kwargs)
#         return response
#
#     return wrap


def register_user(request):
    form = UserRegistrationForm(request.POST or None)
    if request.method == 'GET' or not form.is_valid():
        return render(request, 'registration.html', {'registration_form': form})
    if form.is_valid():
        print(form.cleaned_data)
        data = {}
        data['name'] = form.cleaned_data['name']
        data['username'] = form.cleaned_data['username']
        data['password'] = form.cleaned_data['password2']
        data['balance'] = 0.00
        response = requests.post(BASE_API + 'registration/', data=data)
        if response.status_code != 201:
            return render(request, 'registration_rejected.html')
        else:
            return render(request, 'registration_success.html')
    else:
        return render(request, 'registration.html', {'registration_form': form})


def login_user(request):
    # auth = request.COOKIES.get('auth')
    # if auth:
    #     return redirect('index')
    form = UserLoginForm(request.POST or None)
    next_url = request.GET.get('next') or reverse('index')
    if request.method == 'GET' or not form.is_valid():
        return render(request, 'login.html', {'login_form': form, 'next': next_url})
    if form.is_valid():
        print(form.cleaned_data)
        response = requests.post(BASE_API + 'login/', data=form.cleaned_data)
        if response.status_code != 201 and response.status_code != 409:
            return render(request, 'login.html',
                          {'login_form': form, 'next': next_url, 'login_message': 'Login failed'})
        response_json = response.json()
        authenticator = response_json['auth']
        next_url = reverse('index')
        response = HttpResponseRedirect(next_url)
        response.set_cookie('auth', authenticator)
        return response


def logout_user(request):
    auth = request.COOKIES.get('auth')
    if auth:
        response = requests.delete(BASE_API + 'logout/' + auth + '/')
        if response.status_code == 204:
            return render(request, 'logout.html', {'log_message': 'Logout successful'})
        else:
            return render(request, 'logout.html', {'log_message': 'Logout failed'})
    response = HttpResponseRedirect(reverse('index'))
    response.delete_cookie('auth')
    return response


def create_carpool(request):
    auth = request.COOKIES.get('auth')
    if not auth:
        return HttpResponseRedirect(reverse('login') + '?next=' + reverse('create_carpool'))
    form = CreateCarpoolForm(request.POST or None)
    next_url = reverse('index')
    if request.method == 'GET' or not form.is_valid():
        return render(request, 'create_carpool.html', {'createCarpoolForm': form, 'next': next_url})
    if form.is_valid():
        response = requests.post(BASE_API + 'carpools/', data=form.cleaned_data)
        response_json = response.json()
        print(response_json)
        if response.status_code == 201:
            return render(request, 'carpool_response.html',
                          {'createCarpoolForm': form, 'next': next_url, 'detail': 'Carpool successfully created.'})
        else:
            return render(request, 'create_carpool.html',
                          {'createCarpoolForm': form, 'next': next_url, 'error_message': response_json.get('detail')})


def search_carpools(request):
    search_form = SearchForm(request.POST or None)
    next_url = reverse('index') or request.GET.get('next')
    if request.method == 'GET':
        return render(request, 'search.html', {'search_form': search_form, 'next': next_url})
    if search_form.is_valid():
        response = requests.post(BASE_API + 'search/', data=json.dumps({'query': search_form.cleaned_data['search']}))
        response_json = response.json()
        print(response_json)
        return render(request, 'search_result.html', {'data': response_json})
