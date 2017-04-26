import json

from django.test import TestCase, Client


class UserTestCase(TestCase):
    def setUp(self):
        """
        setUp method is called before each test
        """
        self.client = Client()

    def test_post_user(self):
        """
        checks that res contains parameter order list & implicitly
        checks that the HTTP status code is 200
        """
        body = 'name=Abc+Def&username=abcdef&password=abcdef&balance=12.00'
        res = self.client.post('/v1/users/', body, 'application/json')
        self.assertEqual(res.status_code, 201)

    def test_get_user(self):
        body = 'name=Abc+Def&username=abcdef&password=abcdef&balance=12.00'
        res = self.client.post('/v1/users/', body, 'application/json')
        res = self.client.get('/v1/users/0/')
        self.assertNotEqual(res.status_code, 200)
        res = self.client.get('/v1/users/')
        res_json = json.loads(res.content.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_json['data']['count'], 1)

    def tearDown(self):
        self.client = None


class CarpoolTestCase(TestCase):
    def setUp(self):
        """
        setUp method is called before each test
        """
        self.client = Client()

    def test_post_carpool(self):
        """
        checks that res contains parameter order list & implicitly
        checks that the HTTP status code is 200
        """
        body = 'name=Abc+Def&username=abcdef&password=abcdef&balance=12.00'
        self.client.post('/v1/users/', body, 'application/json')
        get_res = self.client.get('/v1/users/1/')
        self.assertEqual(get_res.status_code, 200)
        post_res = self.client.post('/v1/carpools/', {'driver': 1,
                                                      'cost': 5.00,
                                                      'location_start_lat': 38.385,
                                                      'location_start_lon': -77.385,
                                                      'location_end_lat': 39.834,
                                                      'location_end_lon': -78.80,
                                                      'time_leaving': 1.30,
                                                      'time_arrival': 1.50})
        self.assertEqual(post_res.status_code, 400)

    def test_get_carpool(self):
        res = self.client.get('/v1/carpools/0/')
        res_json = json.loads(res.content.decode('utf-8'))
        self.assertEqual(res.status_code, 401)

    def tearDown(self):
        self.client = None
