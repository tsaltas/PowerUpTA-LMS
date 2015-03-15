#from rest_framework.test import APIClient
import json

from django.core.urlresolvers import reverse

from django.shortcuts import get_object_or_404

from rest_framework.test import APITestCase, APIRequestFactory

from rest_framework import status

from lessons.models import Activity, Material

"""
NOTE:

By default CSRF validation is not applied when using APIClient.
If you need to explicitly enable CSRF validation, you can do so by
setting the enforce_csrf_checks flag when instantiating the client.

factory = APIRequestFactory(enforce_csrf_checks=True)

As usual CSRF validation will only apply to any session authenticated views.
This means CSRF validation will only occur if the client has been logged in by calling login().
"""

"""
EXAMPLES:

factory = APIRequestFactory()
request = factory.post('/notes/', {'title': 'new idea'})

client = APIClient()
client.post('/notes/', {'title': 'new idea'}, format='json')
"""

class MaterialTests(APITestCase):
	@classmethod
	def setUpClass(cls):
		"""
		Fake objects to be used across all tests in this class
		"""
		# Create some activity objects to associate with materials
		activity1 = Activity.objects.create(
			name="TestActivity1"
			, description="This is a test activity."
		)

		activity2 = Activity.objects.create(
			name="TestActivity2"
			, description="This is another test activity."
		)

		# Crate some materials objects
		Material.objects.create(
			name='Test1'
			, url='http://www.test1.com'
		)
		material2 = Material.objects.create(
			name='Test2'
			, url='http://www.test2.com'
		)
		material2.activities.add(activity1)
		material2.save()

		material3 = Material.objects.create(
			name='Test3'
			, url='http://www.test3.com'
		)
		material3.activities.add(activity1)
		material3.activities.add(activity2)
		material2.save()

		# Data to compare against objects returned from the API
		cls.data1 = {
			'id': 1
			, 'name': 'Test1'
			, 'url': 'http://www.test1.com'
			, 'activities': []
		}
		cls.data2 = {
			'id': 2
			, 'name': 'Test2'
			, 'url': 'http://www.test2.com'
			, 'activities': [1]
		}
		cls.data3 = {
			'id': 3
			, 'name': 'Test3'
			, 'url': 'http://www.test3.com'
			, 'activities': [1, 2]
		}
	
	@classmethod
	def tearDownClass(cls):
		"""
		Delete objects
		"""
		Activity.objects.all().delete()
		Material.objects.all().delete()

	def test_create_material(self):
		"""
		Should be able to create a new material object with valid data.
		"""
		url = reverse('lessons:material-list')

		# 0 activities
		data4 = {
			'name': 'Test4'
			, 'url': 'http://www.test4.com'
			, 'activities': []
		}
		# 1 activity
		data5 = {
			'name': 'Test5'
			, 'url': 'http://www.test5.com'
			, 'activities': [1]
		}
		# >1 activities
		data6 = {
			'name': 'Test6'
			, 'url': 'http://www.test6.com'
			, 'activities': [1, 2]
		}

		response4 = self.client.post(url, data4, format='json')
		response5 = self.client.post(url, data5, format='json')
		response6 = self.client.post(url, data6, format='json')

		self.assertEqual(response4.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response5.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response6.status_code, status.HTTP_201_CREATED)

		# API should include new material ID number in response
		data4['id'] = 4
		data5['id'] = 5
		data6['id'] = 6

		self.assertEqual(response4.data, data4)
		self.assertEqual(response5.data, data5)
		self.assertEqual(response6.data, data6)

	def test_create_material_invalid_data(self):
		"""
		Should NOT be able to create a new material object with invalid data.
		"""
		url = reverse('lessons:material-list')

		# name missing
		data4 = {
			'name': ''
			, 'url': 'http://www.test4.com'
			, 'activities': []
		}
		# URL missing
		data5 = {
			'name': 'Test5'
			, 'url': ''
			, 'activities': []
		}
		# URL malformed
		data6 = {
			'name': 'Test6'
			, 'url': 'www.test6.com'
			, 'activities': []
		}
		# URL malformed
		data7 = {
			'name': 'Test7'
			, 'url': 'test7.com'
			, 'activities': []
		}
		# URL malformed
		data8 = {
			'name': 'Test8'
			, 'url': 'test8.co'
			, 'activities': []
		}
		# Activity DNE
		data9 = {
			'name': 'Test9'
			, 'url': 'http://www.test9.com'
			, 'activities': [4]
		}

		response4 = self.client.post(url, data4, format='json')
		response5 = self.client.post(url, data5, format='json')
		response6 = self.client.post(url, data6, format='json')
		response7 = self.client.post(url, data7, format='json')
		response8 = self.client.post(url, data8, format='json')
		response9 = self.client.post(url, data9, format='json')

		self.assertEqual(response4.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response5.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response6.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response7.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response8.status_code, status.HTTP_400_BAD_REQUEST)
		# Activity DNE, so should return 404 not found
		self.assertEqual(response9.status_code, status.HTTP_404_NOT_FOUND)

		# API should include new material ID number in response
		data4['id'] = 4
		data5['id'] = 5
		data6['id'] = 6
		data7['id'] = 7
		data8['id'] = 8
		data9['id'] = 9

		self.assertEqual(response4.data, {'name': ['This field may not be blank.']})
		self.assertEqual(response5.data, {'url': ['This field may not be blank.']})
		self.assertEqual(response6.data, {'url': ['Enter a valid URL.']})
		self.assertEqual(response7.data, {'url': ['Enter a valid URL.']})
		self.assertEqual(response8.data, {'url': ['Enter a valid URL.']})
		self.assertEqual(response9.data, {'detail': 'Not found'})

	def test_get_all_materials(self):
		"""
		Should be able to get list of materials
		"""
		url = reverse('lessons:material-list')

		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 3)

		# Convert ordered dict objects into unordered dicts for comparison
		self.assertEqual(dict(response.data[0]), self.data1)
		self.assertEqual(dict(response.data[1]), self.data2)
		self.assertEqual(dict(response.data[2]), self.data3)

	# try GET object that exists
	# try GET object that DNE
	# try POST duplicate name
	# try PUT bad data
	# try PUT good data
	# try PUT on object that DNE
	# try DELETE object that exists
	# try DELETE on object that DNE
	# check relationships with other objects
	# material associated with existing activity
	# try with activity that DNE
	# try leaving out any activity
	# try passing in multiple activities