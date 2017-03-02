import requests
from django.http import JsonResponse

MODEL_API = 'http://model-api:8000/'


def index(request):
    if request.method == 'GET':
        return JsonResponse({'status': '200 OK', 'message': 'This is the experience API entry point.'}, status=200)


def get_user_detail(request, pk):
    if request.method == 'GET':
        response = requests.get(MODEL_API + 'v1/users/' + pk + '/').json()
        if response['status'] == '200 OK':
            return JsonResponse(response)
        else:
            return response['message']


def get_users(request):
    if request.method == 'GET':
        response = requests.get(MODEL_API + 'v1/users/').json()
        return JsonResponse(response)


def get_latest_data(request):
    if request.method == 'GET':
        data = {}
        carpools_response = requests.get(MODEL_API + 'v1/carpools/').json()
        users_response = requests.get(MODEL_API + 'v1/users/').json()
        if carpools_response and users_response:
            data['carpools'] = carpools_response['data']
            data['users'] = users_response['data']
            return JsonResponse(data, safe=False, status=200)
