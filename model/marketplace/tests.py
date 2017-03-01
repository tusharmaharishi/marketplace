from django.test import TestCase, Client
from django.core.urlresolvers import reverse
import unittest, json, time
from app import User

class GetUserTestCase(TestCase):
	def setUp(self):
		pass #nothing to set up

	def success_response(self):
        #assumes user with id 1 is stored in db
        response = self.client.get(reverse('list_users', kwargs={'pk':'1'}))
        #checks that response contains parameter order list & implicitly
        # checks that the HTTP status code is 200
        self.assertContains(response, 'pk')
        self.assertEqual(response.status_code, 200)

    #user_id not given in url, so error
    def fails_invalid(self):
        response = self.client.get(reverse('list_users', kwargs={'pk':'0'}))
        jsonResponse = json.loads(str(response.content, encoding='utf8'))
        self.assertEquals(jsonResponse["status"], False)
        self.assertEquals(response.status_code, 404)

    def user_fields(self):
    	response = self.client.get(reverse('list_users', kwargs={'pk': '1'}))
    	jsonResponse = json.loads(str(response.content, encoding='utf8'))
    	self.assertEquals(jsonResponse["status"], True)
    	self.assertContains(response, 'pk')
    	self.assertContains(response, 'name')
    	self.assertContains(response, 'balance')

    #tearDown method is called after each test
    def tearDown(self):
        pass #nothing to tear down

class GetCarpoolTestCase
