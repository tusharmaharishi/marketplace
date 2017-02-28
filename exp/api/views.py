from rest_framework.views import APIView
import requests


MODEL_API = 'http://model-api:8000/v1/'

# user registers with a carpool

class UserListByTimeandLocation(APIView):
    pass


class CarpoolListByTimeandLocation(APIView):
    location_start = 10.0
    time_leaving = 12.30

    def get(self, request, time_arrival, location_end):
        if request.method == 'GET':
            res = requests.get(MODEL_API + 'carpools/').json()


