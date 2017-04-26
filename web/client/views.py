import requests
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from kafka import KafkaProducer
from requests.compat import urljoin

from .forms import UserLoginForm, UserRegistrationForm, CreateCarpoolForm

BASE_API = 'http://exp-api:8000/v1/'  # in docker VM, but in root computer, it's localhost:8002/v1/
producer = KafkaProducer(bootstrap_servers='kafka:9092', retries=5)


def get_home_page(request):
    auth_token = request.COOKIES.get('auth_token')
    print('home page', auth_token)
    if auth_token:
        return render(request, 'index.html', {'auth_token': auth_token})
    else:
        return render(request, 'index.html')
    # try:
    #     response = requests.get(BASE_API + 'carpools/').json()
    # except requests.exceptions.RequestException:
    #     return render(request, 'index.html')
    # carpools = response['carpools']
    # users = response['users']
    # for carpool in carpools:
    #     producer.send('new-listings-topic', json.dumps(carpool).encode('utf-8'))
    # return render(request, 'index.html', {'latest_rides': carpools, 'latest_drivers': users})


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


def register_user(request):
    auth = request.COOKIES.get('auth_token')
    if auth:
        return redirect('index')
    form = UserRegistrationForm(request.POST or None)
    if request.method == 'GET' or not form.is_valid():
        return render(request, 'registration.html', {'registration_form': form})
    if form.is_valid():
        data = {'username': form.cleaned_data['username'], 'password': form.cleaned_data['password2'],
                'name': form.cleaned_data['name'], 'balance': 0.00}
        try:
            res = requests.post(urljoin(BASE_API, 'auth/registration/'), data=data)
        except requests.exceptions.RequestException:
            return redirect('index')
        if res.status_code // 100 == 2:
            return render(request, 'registration_success.html')
        else:
            return render(request, 'registration_rejected.html')
    else:
        return render(request, 'registration.html', {'registration_form': form})


def login_user(request):
    http_res = None
    auth_token = request.COOKIES.get('auth_token')
    if auth_token:
        return redirect('index')
    form = UserLoginForm(request.POST or None)
    next_url = request.GET.get('next') or reverse('index')
    if request.method == 'GET' or not form.is_valid():
        return render(request, 'login.html', {'login_form': form, 'next': next_url})
    if form.is_valid():
        print(form.cleaned_data)
        res = requests.post(BASE_API + 'auth/login/', data=form.cleaned_data)
        if res.status_code != 201 and res.status_code != 409:
            return render(request, 'login.html',
                          {'login_form': form, 'next': next_url, 'login_message': 'Login failed'})
        res_json = res.json()
        auth_token = res_json['auth_token']
        http_res = HttpResponseRedirect(reverse('index'))
        http_res.set_cookie('auth_token', auth_token)
        return http_res
    else:
        return render(request, 'login.html',
                      {'login_form': form, 'next': next_url, 'login_message': str(dict(form.errors.items()))})


def logout_user(request):
    http_res = None
    auth_token = request.COOKIES.get('auth_token')
    print('client logout_user', auth_token)
    if auth_token:
        try:
            res = requests.delete(urljoin(BASE_API, 'auth/logout/' + auth_token))
            if res.status_code // 100 == 2:
                http_res = render(request, 'logout.html', {'log_message': 'Logout successful'})
            else:
                http_res = render(request, 'logout.html', {'log_message': 'Logout failed'})
        except requests.exceptions.RequestException:
            return redirect('index')
    # http_res = HttpResponseRedirect(reverse('login'))
    print('deleting cookie')
    http_res.delete_cookie('auth_token')
    return http_res


def create_carpool(request):
    """
    Post auth_token along with form.data
    :param request:
    :return:
    """
    auth_token = request.COOKIES.get('auth_token')
    print(auth_token)
    if not auth_token:
        return HttpResponseRedirect(reverse('login') + '?next=' + reverse('create_carpool'))
    form = CreateCarpoolForm(request.POST or None)
    next_url = reverse('index')
    if request.method == 'GET' or not form.is_valid():
        return render(request, 'create_carpool.html', {'createCarpoolForm': form, 'next': next_url})
    if form.is_valid():
        data = form.cleaned_data.copy()
        data['auth_token'] = auth_token
        try:
            res = requests.post(urljoin(BASE_API, 'carpools/'), data=data)
            print('in client', res.status_code)
        except requests.exceptions.RequestException:
            return render(request, 'create_carpool.html', {'createCarpoolForm': form, 'next': next_url})
        res_json = res.json()
        if res.status_code // 100 == 2:
            return render(request, 'carpool_response.html',
                          {'createCarpoolForm': form, 'next': next_url, 'detail': 'Carpool successfully created.'})
        else:
            return render(request, 'create_carpool.html',
                          {'createCarpoolForm': form, 'next': next_url, 'error_message': res_json.get('detail')})
    else:
        return render(request, 'create_carpool.html',
                      {'createCarpoolForm': form, 'next': next_url, 'error_message': str(dict(form.errors.items()))})


def search_carpools(request):
    if request.GET.get('search_box') is not None:
        params = {'keywords': request.GET.get('search_box', None)}
        results = []
        try:
            res = requests.get(BASE_API + 'search', params=params)
        except requests.exceptions.RequestException:
            return render(request, 'search.html')
        res_json = res.json()
        hits = res_json['data']['hits']
        total = res_json['data']['total']
        for hit in hits:
            results.append(hit['_source'])
        if results:
            return render(request, 'search_result.html', {'results': results, 'total': total})
        else:
            return render(request, 'search_result.html')
    else:
        return render(request, 'search.html')

        # search_form = SearchForm(request.POST or None)
        # next_url = reverse('index') or request.GET.get('next')
        # if request.method == 'GET' or not search_form.is_valid():
        #     return render(request, 'search.html', {'search_form': search_form, 'next': next_url})
        # if search_form.is_valid():
        #     results = []
        #     response = requests.post(BASE_API + 'search', params={'keywords': search_form.cleaned_data['search']})
        #     if response:
        #         res_json = response.json()
        #         for hit in res_json['hits']['hits']:
        #             results.append(hit['_source'])
