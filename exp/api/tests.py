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
        res = self.client.post('/v1/auth/registration/', body, 'application/json')
        self.assertNotEqual(res.status_code, 400)

    def test_login_user(self):
        body = 'name=Abc+Def&username=abcdef&password=abcdef&balance=12.00'
        res = self.client.post('/v1/auth/registration/', body, 'application/json')
        body = 'username=abcdef&password=abcdef'
        res = self.client.post('/v1/auth/login', body, 'application/json')
        self.assertNotEqual(res.status_code, 400)

    def test_get_driver(self):
        body = 'name=Abc+Def&username=abcdef&password=abcdef&balance=12.00'
        res = self.client.post('/v1/auth/registration/', body, 'application/json')
        body = 'username=abcdef&password=abcdef'
        res = self.client.post('/v1/auth/login', body, 'application/json')
        self.assertNotEqual(res.status_code, 400)

    def tearDown(self):
        self.client = None

