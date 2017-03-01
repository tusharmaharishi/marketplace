import json

from django.core.urlresolvers import reverse
from django.test import TestCase


class GetUserTestCase(TestCase):
    def setUp(self):
        pass  # nothing to set up

    def test_success_response(self):
        # assumes user with id 1 is stored in db
        response = self.client.get(reverse('user_list'))
        # checks that response contains parameter order list & implicitly
        # checks that the HTTP status code is 200
        jsonResponse = json.loads(str(response.content, encoding='utf8'))
        self.assertEquals(jsonResponse["status"], '200 OK')
        self.assertContains(response, 'pk')
        self.assertEqual(response.status_code, 200)

    def test_fails_invalid(self):
        response = self.client.get(reverse('user_detail', kwargs={'pk': 0}))
        jsonResponse = json.loads(str(response.content, encoding='utf8'))
        self.assertEquals(jsonResponse["status"], '404 Not Found')
        self.assertEquals(response.status_code, 404)

    def test_user_fields(self):
        response = self.client.get(reverse('user_detail', kwargs={'pk': 1}))
        jsonResponse = json.loads(str(response.content, encoding='utf8'))
        self.assertEquals(jsonResponse["status"], '200 OK')
        self.assertContains(response, 'pk')
        self.assertContains(response, 'name')
        self.assertContains(response, 'balance')

        # tearDown method is called after each test

    def tearDown(self):
        pass  # nothing to tear down
