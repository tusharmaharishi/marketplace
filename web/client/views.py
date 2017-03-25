import requests
import urllib.request, json
from .forms import LoginForm, RegistrationForm, CreateCarpoolForm
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.template.defaulttags import register

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


def login(request):
    login_form  = LoginForm
    next = request.GET.get('next') #or reverse('home')

    if request.method == 'GET':
        return render(request, 'login.html', {'login_form':login_form, 'next': next})

    f = login_form(request.POST)

    if not f.is_valid(): #what does this do?
        return render(request, 'login.html', {'login_form':login_form, 'next': next})

    username = f.cleaned_data['username']
    password = f.cleaned_data['password']

    data = {'username': username, 'password': password}

    url = BASE_API + 'login/'
    data = urllib.parse.urlencode(data)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    ret = response.read().decode('utf-8')
    resp = json.loads(ret)
    #resp = json.loads(urllib.request.urlopen(urllib.request.Request(url, data)).read().decode('utf-8'))

    if not resp or not resp['status']:
        return render(request, 'login.html', {'login_form': login_form, 'next': next, 'login_message': 'login failed'})

    authenticator = resp['auth']
    response = HttpResponseRedirect(next)
    response.set_cookie("auth", authenticator)
    return  response


def logout(request):
    url = BASE_API + "logout/"
    response = HttpResponseRedirect(reverse('index.html'))    
    auth = request.COOKIES.get('auth')
    response.delete_cookie('auth')
    authpass = {'auth':auth}

    data = urllib.parse.urlencode(authpass)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    ret = response.read().decode('utf-8')
    resp = json.loads(ret)
    if(resp['status'] == True):
        return render(request, "logout.html", {'log_message':'Logout successfuk'})
    else:
        return render(request, "logout.html", {'log_message':'Logout failure'})


def create_carpool(request):
    createCarpoolForm = CreateCarpoolForm()
    next = reverse('index.html')
    auth = request.COOKIES.get('auth')
    if not auth:
        return HttpReseponseRedirect(reverse("login") + "?next=" + reverse("create_carpool"))
    if request.method == "GET":
        return render(request, 'create_carpool.html', {'createCarpoolForm':createCarpoolForm, 'next':next})

    form = CreateCarpoolForm(request.POST)
    if not form.is_valid():
        return render(request, 'create_carpool.html', {'createCarpoolForm':createCarpoolForm, 'next':next})

    driver = form.cleaned_data['driver']
    #passengers = form.cleaned_data['passengers']
    cost = form.cleaned_data['cost']
    location_start = form.cleaned_data['location_start']
    location_end = form.cleaned_data['location_end']
    time_leaving = form.cleaned_data['time_leaving']
    time_arrival = form.cleaned_data['time_arrival']

    data = {"driver" : driver,
            "cost" : cost,
            "location_start" : location_start,
            "location_end" : location_end,
            "time_leaving" : time_leaving,
            "time_arrival" : time_arrival}

    url = BASE_API + 'create_carpool/'
    data = urllib.parse.urlencode(data)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    ret = response.read().decode('utf-8')
    resp = json.loads(ret)
    if resp and not resp['status']:
        return render(request, "carpool_response.html", {'createCarpoolForm': createCarpoolForm, 'next': next, 'message': "Carpool failed to be created. Are you logged in?"})
    return render(request, "carpool_response.html", {'createCarpoolForm': createCarpoolForm, 'next': next, 'message': "Carpool successfully created."})

def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = {'username': form.cleaned_data['username'],
                    'password': form.cleaned_data["password1"]}
            url = BASE_API + 'registration/'
            data = urllib.parse.urlencode(data)
            data = data.encode('utf-8')
            req = urllib.request.Request(url, data)
            response = urllib.request.urlopen(req)
            ret = response.read().decode('utf-8')
            new_user = json.loads(ret)
            if new_user['status'] is False:
                return render(request, "registration_rejected.html")
            else:
                return render(request, "registration_success.html")

        else:
            form = RegistrationForm()
        return render(request, "registration.html", {'registration_form': form})



















