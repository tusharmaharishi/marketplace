import json

from django.test import TestCase, Client

BASE_API = 'http://model-api:8000/'


class GetUserTestCase(TestCase):
    def setUp(self):
        """
        setUp method is called before each test
        """
        self.client = Client()

    def test_respond_success(self):
        """
        checks that response contains parameter order list & implicitly
        checks that the HTTP status code is 200
        """
        self.client.post('/v1/users/', {'name': 'Aa', 'balance': 12.00})
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertContains(response, 'data')
        self.assertEqual(response_json['count'], 1)

    def test_respond_failure(self):
        response = self.client.get('/v1/users/0/')
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_json['message'], 'This user does not exist.')

    def test_post_user(self):
        """
        assumes no users are stored in db before POST
        """
        response = self.client.post('/v1/users/', {'name': 'Aa', 'balance': 10.00})
        self.assertEqual(response.status_code, 201)
        response_json = json.loads(str(response.content, encoding='utf8'))
        user = response_json['data'][0]
        self.assertTrue(user['pk'] > 0)
        self.assertEqual(user['fields']['name'], 'Aa')
        self.assertEqual(float(user['fields']['balance']), 10.00)

    def test_get_users(self):
        self.client.post('/v1/users/', {'name': 'Aa', 'balance': 12.00})
        self.client.post('/v1/users/', {'name': 'Bb', 'balance': 15.00})
        response = self.client.get('/v1/users/')
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['count'], 2)
        users = response_json['data']
        self.assertEqual(users[0]['fields']['name'], 'Aa')
        self.assertEqual(float(users[0]['fields']['balance']), 12.00)
        self.assertEqual(users[1]['fields']['name'], 'Bb')
        self.assertEqual(float(users[1]['fields']['balance']), 15.00)

    # def test_put_users(self):
    #     self.client.post('/v1/users/', {'name': 'Aa', 'balance': 10.00})
    #     self.post

    def tearDown(self):
        pass  # nothing to tear down


class GetCarpoolTestCase(TestCase):
    def setUp(self):
        """
        setUp method is called before each test
        """
        self.client = Client()

    def test_respond_success(self):
        """
        checks that response contains parameter order list & implicitly
        checks that the HTTP status code is 200
        """
        self.client.post('/v1/users/', {'name': 'Aa', 'balance': 10.00})
        get_response = self.client.get('/v1/users/7/')
        self.assertEqual(get_response.status_code, 200)
        post_response = self.client.post('/v1/carpools/', {'driver': 7,
                                                           'cost': 5.00,
                                                           'location_start': 20.385,
                                                           'location_end': 21.834,
                                                           'time_leaving': 1.30,
                                                           'time_arrival': 1.50})
        self.assertEqual(post_response.status_code, 201)
        response = self.client.get('/v1/carpools/')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertContains(response, 'data')
        self.assertEqual(response_json['count'], 1)

    def test_respond_failure(self):
        response = self.client.get('/v1/carpools/0/')
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_json['message'], 'This carpool does not exist.')

    def test_post_carpool(self):
        """
        assumes Aa is driver and is stored in db before POST
        """
        self.client.post('/v1/users/', {'name': 'Aa', 'balance': 10.00})
        get_response = self.client.get('/v1/users/3/')
        self.assertEqual(get_response.status_code, 200)
        post_response = self.client.post('/v1/carpools/', {'driver': 3,
                                                           'cost': 5.00,
                                                           'location_start': 20.385,
                                                           'location_end': 21.834,
                                                           'time_leaving': 1.30,
                                                           'time_arrival': 1.50})
        self.assertEqual(post_response.status_code, 201)
        response_json = json.loads(str(get_response.content, encoding='utf8'))
        data = response_json['data'][0]
        self.assertEqual(data['fields']['carpool_owned'], None)

    def test_put_carpool(self):
        """
        Bb creates a carpool as driver, Aa and Cc join that carpool with pk 1
        """
        self.client.post('/v1/users/', {'name': 'Aa', 'balance': 10.00})
        self.client.post('/v1/users/', {'name': 'Bb', 'balance': 12.00})
        self.client.post('/v1/users/', {'name': 'Cc', 'balance': 15.00})
        response = self.client.get('/v1/users/4/')
        self.assertEqual(response.status_code, 200)
        self.client.post('/v1/carpools/', {'driver': 4,
                                           'cost': 5.00,
                                           'location_start': 20.385,
                                           'location_end': 21.834,
                                           'time_leaving': 1.30,
                                           'time_arrival': 1.50})
        self.client.put('/v1/users/', {'name': 'Aa',
                                       'balance': 10.00,
                                       'carpool_joined': 1})
        self.client.put('/v1/users/', {'name': 'Cc',
                                       'balance': 15.00,
                                       'carpool_joined': 1})
        response = self.client.get('/v1/carpools/3/')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(str(response.content, encoding='utf8'))
        data = response_json['data'][0]
        self.assertEqual(data['fields']['driver'], 4)
        self.assertEqual(data['fields']['passengers'], [])

    def test_delete_carpool(self):
        self.client.post('/v1/users/', {'name': 'Aa', 'balance': 10.00})
        self.client.post('/v1/users/', {'name': 'Bb', 'balance': 12.00})
        self.client.post('/v1/carpools/', {'driver': 2,
                                           'cost': 5.00,
                                           'location_start': 20.385,
                                           'location_end': 21.834,
                                           'time_leaving': 1.30,
                                           'time_arrival': 1.50})
        self.client.put('/v1/users/', {'name': 'Aa',
                                       'balance': 10.00,
                                       'carpool_joined': 1})
        delete_response = self.client.delete('/v1/carpools/1/')
        self.assertEqual(delete_response.status_code, 204)
        driver_response = self.client.get('/v1/users/2/')
        pass_response = self.client.get('/v1/users/1/')
        driver_response_json = json.loads(str(driver_response.content, encoding='utf8'))
        pass_response_json = json.loads(str(pass_response.content, encoding='utf8'))
        driver = driver_response_json['data'][0]
        passenger = pass_response_json['data'][0]
        self.assertEqual(driver['fields']['carpool_owned'], None)
        self.assertEqual(passenger['fields']['carpool_joined'], None)

    def tearDown(self):
        pass
