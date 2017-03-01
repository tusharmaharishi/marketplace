import json

from django.test import TestCase, Client

BASE_API = 'http://model-api:8000/'


class GetUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_success_response(self):
        # assumes user with id 1 is stored in db
        response = self.client.get('/v1/users/')
        # checks that response contains parameter order list & implicitly
        # checks that the HTTP status code is 200
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'count')
        self.assertContains(response, 'data')

    def test_fail_response(self):
        response = self.client.get('/v1/users/0/')
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response_json['status'], '404 Not Found')
        self.assertEqual(response.status_code, 404)

    def test_user_get(self):
        response = self.client.get('/v1/users/1/')
        response_json = json.loads(str(response.content, encoding='utf8'))
        data = response_json['data'][0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['pk'], 1)
        # self.assertContains(response_json['data']['fields']['name'], 'Kevin')
        # self.assertContains(response_json['data'], 'balance')
        # tearDown method is called after each test

    # def test_user_post(self):
    #     response = self.client.post('/v1/users/', {'name': 'Tester', 'balance': 10.00})
    #


    def tearDown(self):
        pass  # nothing to tear down


class GetCarpoolTestCAse(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass
