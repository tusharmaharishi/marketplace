import json

import requests
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegistrationForm, CreateCarpoolForm

BASE_API = 'http://exp-api:8000/v1/'  # in docker VM, but in root computer, it's localhost:8002/v1/


def get_carpools_latest(request):
    # response = requests.get(BASE_API + 'latest/').json()
    # data = response['carpools']
    return render(request, 'index.html')


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


def login_required(f):
    def wrap(request, *args, **kwargs):
        next_url = reverse('index')
        response = HttpResponseRedirect(next_url)
        auth = request.COOKIES.get("auth")
        if auth:
            response = requests.get('http://exp-api:8000/api/v1/authenticate/' + str(auth)).json()
            if response['status'] == 200:
                return f(request, *args, **kwargs)
        return response

    return wrap


def register_user(request):
    auth = request.COOKIES.get('auth')
    if auth:
        return redirect('index')
    form = UserRegistrationForm(request.POST or None)
    if request.method == 'GET' or not form.is_valid():
        return render(request, "registration.html", {'registration_form': form})
    if form.is_valid():
        print('IN WEB {}'.format(form.cleaned_data))
        print('IN WEB {}'.format(requests.post(BASE_API + 'registration/', data=json.dumps(form.cleaned_data))))
        # response = requests.post(BASE_API + 'registration/', data=json.dumps(form.cleaned_data)).json()
        # if not response or response['status'] != 200:
        #     return render(request, "registration_rejected.html")
        # else:
        #     return render(request, "registration_success.html")
    return render(request, "registration.html", {'registration_form': form})


def login_user(request):
    auth = request.COOKIES.get('auth')
    if auth:
        return redirect('index')
    form = UserLoginForm(request.POST or None)
    next_url = request.GET.get('next') or reverse('index')
    if request.method == 'GET' or not form.is_valid():
        return render(request, 'login.html', {'login_form': form, 'next': next_url})
    print('in web', json.dumps(form.cleaned_data))

    response = requests.post(BASE_API + 'login/', data=json.dumps(form.cleaned_data)).json()
    print('in web', response)
    if not response or response['status'] != 200:
        return render(request, 'login.html',
                      {'login_form': form, 'next': next_url, 'login_message': 'Login failed'})
    authenticator = response['auth']
    next_url = reverse('index')
    response = HttpResponseRedirect(next_url)
    response.set_cookie('auth', authenticator)
    return response

    # if auth:
    #     return redirect('index')
    # f = login_form(request.POST)
    # next = request.GET.get('next') or reverse('index.html')
    #
    # if request.method == 'GET':
    #     return render(request, 'login.html', {'login_form': login_form, 'next': next})
    #
    # if not f.is_valid():  # what does this do?
    #     return render(request, 'login.html', {'login_form': login_form, 'next': next})
    #
    # username = f.cleaned_data['username']
    # password = f.cleaned_data['password']
    #
    # data = {'username': username, 'password': password}
    #
    # url = BASE_API + 'login/'
    # resp = requests.post(url, data=json.dumps(data))
    # data = urllib.parse.urlencode(data)
    # data = data.encode('utf-8')
    # req = urllib.request.Request(url, data)
    # response = urllib.request.urlopen(req)
    # ret = response.read().decode('utf-8')
    # resp = json.loads(ret)
    # # resp = json.loads(urllib.request.urlopen(urllib.request.Request(url, data)).read().decode('utf-8'))

    authenticator = resp['auth']
    next = reverse('index.html')
    response = HttpResponseRedirect(next)

    response.set_cookie("auth", authenticator)
    return response


def logout_user(request):
    url = BASE_API + "logout/"
    response = HttpResponseRedirect(reverse('index.html'))
    auth = request.COOKIES.get('auth')
    response.delete_cookie('auth')
    authpass = {'auth': auth}

    data = urllib.parse.urlencode(authpass)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    ret = response.read().decode('utf-8')
    resp = json.loads(ret)
    if (resp['status'] == True):
        return render(request, "logout.html", {'log_message': 'Logout successfuk'})
    else:
        return render(request, "logout.html", {'log_message': 'Logout failure'})


def create_carpool(request):
    createCarpoolForm = CreateCarpoolForm()
    next = reverse('index.html')
    auth = request.COOKIES.get('auth')
    if not auth:
        return HttpReseponseRedirect(reverse("login") + "?next=" + reverse("create_carpool"))
    if request.method == "GET":
        return render(request, 'create_carpool.html', {'createCarpoolForm': createCarpoolForm, 'next': next})

    form = CreateCarpoolForm(request.POST)
    if not form.is_valid():
        return render(request, 'create_carpool.html', {'createCarpoolForm': createCarpoolForm, 'next': next})

    driver = form.cleaned_data['driver']
    # passengers = form.cleaned_data['passengers']
    cost = form.cleaned_data['cost']
    location_start = form.cleaned_data['location_start']
    location_end = form.cleaned_data['location_end']
    time_leaving = form.cleaned_data['time_leaving']
    time_arrival = form.cleaned_data['time_arrival']

    data = {"driver": driver,
            "cost": cost,
            "location_start": location_start,
            "location_end": location_end,
            "time_leaving": time_leaving,
            "time_arrival": time_arrival}

    url = BASE_API + 'create_carpool/'
    data = urllib.parse.urlencode(data)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    ret = response.read().decode('utf-8')
    resp = json.loads(ret)
    if resp and not resp['status']:
        return render(request, "carpool_response.html", {'createCarpoolForm': createCarpoolForm, 'next': next,
                                                         'message': "Carpool failed to be created. Are you logged in?"})
    return render(request, "carpool_response.html",
                  {'createCarpoolForm': createCarpoolForm, 'next': next, 'message': "Carpool successfully created."})
