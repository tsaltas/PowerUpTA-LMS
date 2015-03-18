from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from lessons.models import Activity, Resource

class ResourceTests(APITestCase):
	
	""" RESOURCE TEST SETUP / TEARDOWN """

	@classmethod
	def setUpClass(cls):
		"""
		Fake objects to be used across all tests in this class
		"""
		# Endpoint URL for all tests
		cls.url = reverse('lessons:resource-list')

		# Create some activity objects to associate with resources
		activity1 = Activity.objects.create(
			name="TestActivity1"
			, description="This is a test activity."
		)

		activity2 = Activity.objects.create(
			name="TestActivity2"
			, description="This is another test activity."
		)

		# Create some resource objects
		resource1 = Resource.objects.create(
			name='Test1'
			, url='http://www.test1.com'
		)
		resource2 = Resource.objects.create(
			name='Test2'
			, url='http://www.test2.com'
		)
		resource2.activities.add(activity1)

		resource3 = Resource.objects.create(
			name='Test3'
			, url='http://www.test3.com'
		)
		resource3.activities.add(activity1)
		resource3.activities.add(activity2)

		# Add activities to the class object for reference in later tests
		cls.activity1 = activity1
		cls.activity2 = activity2

		# Data to compare against objects returned from the API
		cls.resource1 = {
			'id': 1
			, 'name': 'Test1'
			, 'url': 'http://www.test1.com'
			, 'activities': []
		}
		cls.resource2 = {
			'id': 2
			, 'name': 'Test2'
			, 'url': 'http://www.test2.com'
			, 'activities': [activity1.id]
		}
		cls.resource3 = {
			'id': 3
			, 'name': 'Test3'
			, 'url': 'http://www.test3.com'
			, 'activities': [activity1.id, activity2.id]
		}
	
	@classmethod
	def tearDownClass(cls):
		"""
		Delete objects
		"""
		Activity.objects.all().delete()
		Resource.objects.all().delete()

	""" RESOURCE GET REQUESTS """
	def test_get_all_resources(self):
		"""
		Should be able to GET list of resources
		"""
		response = self.client.get(self.url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 3)

		# Convert ordered dict objects into unordered dicts for comparison
		self.assertEqual(dict(response.data[0]), self.resource1)
		self.assertEqual(dict(response.data[1]), self.resource2)
		self.assertEqual(dict(response.data[2]), self.resource3)

	def test_get_one_resource(self):
		"""
		Should be able to GET a single resource that exists
		"""
		response = self.client.get(self.url + "1/")

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# Convert ordered dict objects into unordered dicts for comparison
		self.assertEqual(response.data, self.resource1)

	def test_get_one_resource_that_DNE(self):
		"""
		Should fail to GET a single resource that does not exist
		"""
		response = self.client.get(self.url + "4/")

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		# Convert ordered dict objects into unordered dicts for comparison
		self.assertEqual(response.data, {'detail': 'Not found'})

	""" RESOURCE POST REQUESTS """
	def test_create_resource(self):
		"""
		Should be able to create a new resource object with valid data.
		"""
		# 0 activities
		resource4 = {
			'name': 'Test4'
			, 'url': 'http://www.test4.com'
			, 'activities': []
		}
		# 1 activity
		resource5 = {
			'name': 'Test5'
			, 'url': 'http://www.test5.com'
			, 'activities': [self.activity1.id]
		}
		# >1 activities
		resource6 = {
			'name': 'Test6'
			, 'url': 'http://www.test6.com'
			, 'activities': [self.activity1.id, self.activity2.id]
		}

		response4 = self.client.post(self.url, resource4, format='json')
		response5 = self.client.post(self.url, resource5, format='json')
		response6 = self.client.post(self.url, resource6, format='json')

		self.assertEqual(response4.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response5.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response6.status_code, status.HTTP_201_CREATED)

		# API should include new resource ID number in response
		resource4['id'] = 4
		resource5['id'] = 5
		resource6['id'] = 6

		self.assertEqual(response4.data, resource4)
		self.assertEqual(response5.data, resource5)
		self.assertEqual(response6.data, resource6)

	def test_create_resource_invalid_data(self):
		"""
		Should NOT be able to create a new resource object with invalid data.
		"""
		# name missing
		resource4 = {
			'name': ''
			, 'url': 'http://www.test4.com'
			, 'activities': [self.activity1.id]
		}
		# URL missing
		resource5 = {
			'name': 'Test5'
			, 'url': ''
			, 'activities': []
		}
		# URL malformed
		resource6 = {
			'name': 'Test6'
			, 'url': 'www.test6.com'
			, 'activities': [self.activity2.id]
		}
		# URL malformed
		resource7 = {
			'name': 'Test7'
			, 'url': 'test7.com'
			, 'activities': []
		}
		# URL malformed
		resource8 = {
			'name': 'Test8'
			, 'url': 'test8.co'
			, 'activities': []
		}
		# Activity DNE
		resource9 = {
			'name': 'Test9'
			, 'url': 'http://www.test9.com'
			, 'activities': [100]
		}

		response4 = self.client.post(self.url, resource4, format='json')
		response5 = self.client.post(self.url, resource5, format='json')
		response6 = self.client.post(self.url, resource6, format='json')
		response7 = self.client.post(self.url, resource7, format='json')
		response8 = self.client.post(self.url, resource8, format='json')
		response9 = self.client.post(self.url, resource9, format='json')

		self.assertEqual(response4.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response5.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response6.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response7.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response8.status_code, status.HTTP_400_BAD_REQUEST)
		# Activity DNE, so should return 404 not found
		self.assertEqual(response9.status_code, status.HTTP_404_NOT_FOUND)

		# API should include new resource ID number in response
		resource4['id'] = 4
		resource5['id'] = 5
		resource6['id'] = 6
		resource7['id'] = 7
		resource8['id'] = 8
		resource9['id'] = 9

		self.assertEqual(response4.data, {'name': ['This field may not be blank.']})
		self.assertEqual(response5.data, {'url': ['This field may not be blank.']})
		self.assertEqual(response6.data, {'url': ['Enter a valid URL.']})
		self.assertEqual(response7.data, {'url': ['Enter a valid URL.']})
		self.assertEqual(response8.data, {'url': ['Enter a valid URL.']})
		self.assertEqual(response9.data, {'detail': 'Not found'})

	def test_create_resource_duplicate_name(self):
		"""
		Should NOT be able to create a new resource object with duplicate value
		on unique-only field "name"
		"""

		# Duplicate name
		duplicate = {
			'name': 'Test1'
			, 'url': 'http://www.duplicate.com'
			, 'activities': []
		}
	
		response = self.client.post(self.url, duplicate, format='json')

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		self.assertEqual(response.data, {'name': ['This field must be unique.']})

	""" RESOURCE PATCH REQUESTS"""
	def test_update_resource(self):
		"""
		Should be able to update resource with PATCH request
		"""

		# Update name
		response1 = self.client.patch(self.url + "1/", {'name': 'Updated'}, format='json')
		resource1 = {
			'id': 1
			, 'name': 'Updated'
			, 'url': 'http://www.test1.com'
			, 'activities': []
		}
		
		# Update URL
		response2 = self.client.patch(self.url + "2/", {'url': 'http://www.updated.com'}, format='json')
		resource2 = {
			'id': 2
			, 'name': 'Test2'
			, 'url': 'http://www.updated.com'
			, 'activities': [self.activity1.id]
		}
		
		# Remove one activity
		response3 = self.client.patch(self.url + "3/", {'activities': [self.activity1.id]}, format='json')
		resource3 = {
			'id': 3
			, 'name': 'Test3'
			, 'url': 'http://www.test3.com'
			, 'activities': [self.activity1.id]
		}

		# Remove all activities
		response4 = self.client.patch(self.url + "3/", {'activities': []}, format='json')
		resource4 = {
			'id': 3
			, 'name': 'Test3'
			, 'url': 'http://www.test3.com'
			, 'activities': []
		}

		# Add first activity
		response5 = self.client.patch(
			self.url + "3/"
			, {'activities': [self.activity1.id]}
			, format='json'
		)
		resource5 = {
			'id': 3
			, 'name': 'Test3'
			, 'url': 'http://www.test3.com'
			, 'activities': [self.activity1.id]
		}

		# Add additional activity
		response6 = self.client.patch(
			self.url + "3/"
			, {'activities': [self.activity1.id, self.activity2.id]}
			, format='json'
		)
		resource6 = {
			'id': 3
			, 'name': 'Test3'
			, 'url': 'http://www.test3.com'
			, 'activities': [self.activity1.id, self.activity2.id]
		}

		self.assertEqual(response1.status_code, status.HTTP_200_OK)
		self.assertEqual(response2.status_code, status.HTTP_200_OK)
		self.assertEqual(response3.status_code, status.HTTP_200_OK)
		self.assertEqual(response4.status_code, status.HTTP_200_OK)
		self.assertEqual(response5.status_code, status.HTTP_200_OK)
		self.assertEqual(response6.status_code, status.HTTP_200_OK)

		self.assertEqual(response1.data, resource1)
		self.assertEqual(response2.data, resource2)
		self.assertEqual(response3.data, resource3)
		self.assertEqual(response4.data, resource4)
		self.assertEqual(response5.data, resource5)
		self.assertEqual(response6.data, resource6)
	
	def test_update_resource_invalid_data(self):
		"""
		Should NOT be able to update resource with PATCH request using invalid data
		"""

		# Remove name
		response1 = self.client.patch(self.url + "1/", {'name': ''}, format='json')
		
		# Remove URL
		response2 = self.client.patch(self.url + "2/", {'url': ''}, format='json')
		
		# Add activity that DNE
		response3 = self.client.patch(self.url + "3/", {'activities': [100]}, format='json')

		# Update to duplicate name
		response4 = self.client.patch(self.url + "1/", {'name': 'Test2'}, format='json')

		self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response3.status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(response4.status_code, status.HTTP_400_BAD_REQUEST)

		self.assertEqual(response1.data, {'name': ['This field may not be blank.']})
		self.assertEqual(response2.data, {'url': ['This field may not be blank.']})
		self.assertEqual(response3.data, {'detail': 'Not found'})
		self.assertEqual(response4.data, {'name': ['This field must be unique.']})

	def test_update_resource_that_DNE(self):
		"""
		Should NOT be able to update resource with PATCH request if it does not exist
		"""

		response = self.client.patch(self.url + "4/", {'name': 'Does not exist'}, format='json')

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(response.data, {'detail': 'Not found'})


	""" RESOURCE DELETE REQUESTS """
	def test_delete_resource(self):
		"""
		Should be able to DELETE a resource object
		"""
		response = self.client.delete(self.url + "1/")

		# Verify object deletion
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(response.data, None)

		# Verify that other objects remain
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 2)

		# Convert ordered dict objects into unordered dicts for comparison
		self.assertEqual(dict(response.data[0]), self.resource2)
		self.assertEqual(dict(response.data[1]), self.resource3)

	def test_delete_resource_that_DNE(self):
		"""
		Should NOT be able to DELETE a resource object that does not exist
		"""
		response = self.client.delete(self.url + "4/")

		# Verify object deletion
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(response.data, {'detail': 'Not found'})

		# Verify that all objects remain
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 3)

		# Convert ordered dict objects into unordered dicts for comparison
		self.assertEqual(dict(response.data[0]), self.resource1)
		self.assertEqual(dict(response.data[1]), self.resource2)
		self.assertEqual(dict(response.data[2]), self.resource3)