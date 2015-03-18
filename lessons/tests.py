import json
import unittest

from django.core.urlresolvers import reverse

from django.core.files.uploadedfile import SimpleUploadedFile
from mock import MagicMock
from django.core.files import File

from django.shortcuts import get_object_or_404

from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from rest_framework import status

from lessons.models import Activity, Curriculum, Material, Resource, Tag
from lessons.views import TagViewSet

from lessons.serializers import CurriculumSerializer, MaterialSerializer, ResourceSerializer, TagSerializer

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
	
	""" MATERIAL TEST SETUP / TEARDOWN """

	@classmethod
	def setUpClass(cls):
		"""
		Fake objects to be used across all tests in this class
		"""
		# Endpoint URL for all tests
		cls.url = reverse('lessons:material-list')

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
		material1 = Material.objects.create(
			name='Test1'
			, url='http://www.test1.com'
		)
		material2 = Material.objects.create(
			name='Test2'
			, url='http://www.test2.com'
		)
		material2.activities.add(activity1)

		material3 = Material.objects.create(
			name='Test3'
			, url='http://www.test3.com'
		)
		material3.activities.add(activity1)
		material3.activities.add(activity2)

		# Add activities to the class object for reference in later tests
		cls.activity1 = activity1
		cls.activity2 = activity2

		# Data to compare against objects returned from the API
		cls.material1 = {
			'id': 1
			, 'name': 'Test1'
			, 'url': 'http://www.test1.com'
			, 'activities': []
		}
		cls.material2 = {
			'id': 2
			, 'name': 'Test2'
			, 'url': 'http://www.test2.com'
			, 'activities': [activity1.id]
		}
		cls.material3 = {
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
		Material.objects.all().delete()

	""" MATERIAL GET REQUESTS """
	def test_get_all_materials(self):
		"""
		Should be able to GET list of materials
		"""
		response = self.client.get(self.url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 3)

		# Convert ordered dict objects into unordered dicts for comparison
		self.assertEqual(dict(response.data[0]), self.material1)
		self.assertEqual(dict(response.data[1]), self.material2)
		self.assertEqual(dict(response.data[2]), self.material3)

	def test_get_one_material(self):
		"""
		Should be able to GET a single material that exists
		"""
		response = self.client.get(self.url + "1/")

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# Convert ordered dict objects into unordered dicts for comparison
		self.assertEqual(response.data, self.material1)

	def test_get_one_material_that_DNE(self):
		"""
		Should fail to GET a single material that does not exist
		"""
		response = self.client.get(self.url + "4/")

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		# Convert ordered dict objects into unordered dicts for comparison
		self.assertEqual(response.data, {'detail': 'Not found'})

	""" MATERIAL POST REQUESTS """
	def test_create_material(self):
		"""
		Should be able to create a new material object with valid data.
		"""
		# 0 activities
		material4 = {
			'name': 'Test4'
			, 'url': 'http://www.test4.com'
			, 'activities': []
		}
		# 1 activity
		material5 = {
			'name': 'Test5'
			, 'url': 'http://www.test5.com'
			, 'activities': [self.activity1.id]
		}
		# >1 activities
		material6 = {
			'name': 'Test6'
			, 'url': 'http://www.test6.com'
			, 'activities': [self.activity1.id, self.activity2.id]
		}

		response4 = self.client.post(self.url, material4, format='json')
		response5 = self.client.post(self.url, material5, format='json')
		response6 = self.client.post(self.url, material6, format='json')

		self.assertEqual(response4.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response5.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response6.status_code, status.HTTP_201_CREATED)

		# API should include new material ID number in response
		material4['id'] = 4
		material5['id'] = 5
		material6['id'] = 6

		self.assertEqual(response4.data, material4)
		self.assertEqual(response5.data, material5)
		self.assertEqual(response6.data, material6)

	def test_create_material_invalid_data(self):
		"""
		Should NOT be able to create a new material object with invalid data.
		"""
		# name missing
		material4 = {
			'name': ''
			, 'url': 'http://www.test4.com'
			, 'activities': [self.activity1.id]
		}
		# URL missing
		material5 = {
			'name': 'Test5'
			, 'url': ''
			, 'activities': []
		}
		# URL malformed
		material6 = {
			'name': 'Test6'
			, 'url': 'www.test6.com'
			, 'activities': [self.activity2.id]
		}
		# URL malformed
		material7 = {
			'name': 'Test7'
			, 'url': 'test7.com'
			, 'activities': []
		}
		# URL malformed
		material8 = {
			'name': 'Test8'
			, 'url': 'test8.co'
			, 'activities': []
		}
		# Activity DNE
		material9 = {
			'name': 'Test9'
			, 'url': 'http://www.test9.com'
			, 'activities': [100]
		}

		response4 = self.client.post(self.url, material4, format='json')
		response5 = self.client.post(self.url, material5, format='json')
		response6 = self.client.post(self.url, material6, format='json')
		response7 = self.client.post(self.url, material7, format='json')
		response8 = self.client.post(self.url, material8, format='json')
		response9 = self.client.post(self.url, material9, format='json')

		self.assertEqual(response4.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response5.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response6.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response7.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response8.status_code, status.HTTP_400_BAD_REQUEST)
		# Activity DNE, so should return 404 not found
		self.assertEqual(response9.status_code, status.HTTP_404_NOT_FOUND)

		# API should include new material ID number in response
		material4['id'] = 4
		material5['id'] = 5
		material6['id'] = 6
		material7['id'] = 7
		material8['id'] = 8
		material9['id'] = 9

		self.assertEqual(response4.data, {'name': ['This field may not be blank.']})
		self.assertEqual(response5.data, {'url': ['This field may not be blank.']})
		self.assertEqual(response6.data, {'url': ['Enter a valid URL.']})
		self.assertEqual(response7.data, {'url': ['Enter a valid URL.']})
		self.assertEqual(response8.data, {'url': ['Enter a valid URL.']})
		self.assertEqual(response9.data, {'detail': 'Not found'})

	def test_create_material_duplicate_name(self):
		"""
		Should NOT be able to create a new material object with duplicate value
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

	""" MATERIAL PATCH REQUESTS"""
	def test_update_material(self):
		"""
		Should be able to update material with PATCH request
		"""
		# Update name
		response1 = self.client.patch(self.url + "1/", {'name': 'Updated'}, format='json')
		material1 = {
			'id': 1
			, 'name': 'Updated'
			, 'url': 'http://www.test1.com'
			, 'activities': []
		}
		
		# Update URL
		response2 = self.client.patch(self.url + "2/", {'url': 'http://www.updated.com'}, format='json')
		material2 = {
			'id': 2
			, 'name': 'Test2'
			, 'url': 'http://www.updated.com'
			, 'activities': [self.activity1.id]
		}
		
		# Remove one activity
		response3 = self.client.patch(self.url + "3/", {'activities': [self.activity1.id]}, format='json')
		material3 = {
			'id': 3
			, 'name': 'Test3'
			, 'url': 'http://www.test3.com'
			, 'activities': [self.activity1.id]
		}

		# Remove all activities
		response4 = self.client.patch(self.url + "3/", {'activities': []}, format='json')
		material4 = {
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
		material5 = {
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
		material6 = {
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

		self.assertEqual(response1.data, material1)
		self.assertEqual(response2.data, material2)
		self.assertEqual(response3.data, material3)
		self.assertEqual(response4.data, material4)
		self.assertEqual(response5.data, material5)
		self.assertEqual(response6.data, material6)
	
	def test_update_material_invalid_data(self):
		"""
		Should NOT be able to update material with PATCH request using invalid data
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

	def test_update_material_that_DNE(self):
		"""
		Should NOT be able to update material with PATCH request if it does not exist
		"""
		response = self.client.patch(self.url + "4/", {'name': 'Does not exist'}, format='json')

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(response.data, {'detail': 'Not found'})

	""" MATERIAL DELETE REQUESTS """
	def test_delete_material(self):
		"""
		Should be able to DELETE a material object
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
		self.assertEqual(dict(response.data[0]), self.material2)
		self.assertEqual(dict(response.data[1]), self.material3)

	def test_delete_material_that_DNE(self):
		"""
		Should NOT be able to DELETE a material object that does not exist
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
		self.assertEqual(dict(response.data[0]), self.material1)
		self.assertEqual(dict(response.data[1]), self.material2)
		self.assertEqual(dict(response.data[2]), self.material3)

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
	def test_get_all_activities(self):
		"""
		Should be able to GET list of activities
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

@unittest.skip("Skip tag testing until image upload issue resolved.")
class TagTests(APITestCase):
	
	""" TAG TEST SETUP / TEARDOWN """

	@classmethod
	def setUpClass(cls):
		"""
		Fake objects to be used across all tests in this class
		"""
		# Endpoint URL for all tests
		cls.url = reverse('lessons:tag-list')

		# Create some activity objects to associate with tags
		activity1 = Activity.objects.create(
			name="TestActivity1"
			, description="This is a test activity."
		)

		activity2 = Activity.objects.create(
			name="TestActivity2"
			, description="This is another test activity."
		)

		# Load test logo to associate with tags
		"""
		FAILED APPROACHES

		test_logo = SimpleUploadedFile(
			name='330.jpeg'
			, content=open('lessons/tests/330.jpeg', 'r+b').read()
			, content_type='image/jpeg'
		)

		test_logo = SimpleUploadedFile(
			name='330.jpeg' 
            , content=b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00'
            , content_type='image/jpeg'
        )
		
		test_logo = File(open('lessons/tests/test_img.jpg'))
		test_logo = File(file('lessons/tests/test_img.jpg'))
		
		test_logo = MagicMock(name='TestLogo', spec=File)
		
		test_logo = open('lessons/tests/330.jpeg')
		
		test_logo = StringIO('GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00'
                     '\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')

		"""

		test_logo = SimpleUploadedFile(
			name='test_img.jpg'
			, content=open('lessons/tests/test_img.jpg', 'r+b').read()
			, content_type='image/jpeg'
		)

		# Create some tag objects
		tag1 = Tag.objects.create(
			name='Test1'
			, logo=test_logo
			, category='LAN'
		)
		tag2 = Tag.objects.create(
			name='Test2'
			, logo=test_logo
			, category='TEC'
		)
		tag2.activities.add(activity1)

		tag3 = Tag.objects.create(
			name='Test3'
			, logo=test_logo
			, category='CON'
		)
		tag3.activities.add(activity1)
		tag3.activities.add(activity2)

		# Add objects to the class object for reference in later tests
		cls.activity1 = activity1
		cls.activity2 = activity2
		cls.test_logo = test_logo

		# Data to compare against objects returned from the API
		cls.tag1 = {
			'id': 1
			, 'name': 'Test1'
			, 'logo': 'lessons/tests/test_img.jpg'
			, 'category': 'Language'
			, 'activities': []
		}
		cls.tag2 = {
			'id': 2
			, 'name': 'Test2'
			, 'logo': 'lessons/tests/test_img.jpg'
			, 'category': 'Technology'
			, 'activities': [activity1.id]
		}
		cls.tag3 = {
			'id': 3
			, 'name': 'Test3'
			, 'logo': 'lessons/tests/test_img.jpg'
			, 'category': 'Concept'
			, 'activities': [activity1.id, activity2.id]
		}
	
	@classmethod
	def tearDownClass(cls):
		"""
		Delete objects
		"""
		Activity.objects.all().delete()
		Tag.objects.all().delete()

	""" TAG GET REQUESTS """
	def test_get_all_tags(self):
		"""
		Should be able to GET list of tags
		"""
		response = self.client.get(self.url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 3)

		# Convert ordered dict objects into unordered dicts for comparison
		self.assertEqual(dict(response.data[0]), self.data1)
		self.assertEqual(dict(response.data[1]), self.data2)
		self.assertEqual(dict(response.data[2]), self.data3)

	
	def test_get_one_tag(self):
		"""
		Should be able to GET a single tag that exists
		"""
		response = self.client.get(self.url + "1/")

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# Convert ordered dict objects into unordered dicts for comparison
		self.assertEqual(response.data, self.data1)

	def test_get_one_tag_that_DNE(self):
		"""
		Should fail to GET a single tag that does not exist
		"""
		response = self.client.get(self.url + "4/")

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		# Convert ordered dict objects into unordered dicts for comparison
		self.assertEqual(response.data, {'detail': 'Not found'})

	""" TAG POST REQUESTS """
	def test_create_tag(self):
		"""
		Should be able to create a new tag object with valid data.
		"""

		# 0 activities
		data4 = {
			'name': 'test4'
			, 'logo': self.test_logo
			, 'csrfmiddlewaretoken' : 'Yj7P6O3m43p2vqoHx2oOacnjAXxSJVUx'
			, 'category': 'DIF'
			, 'activities': []
		}
		
		print "\ntest logo file size (inside tests.py): " + str(self.test_logo.size)

		# 1 activity
		data5 = {
			'name': 'Test5'
			, 'logo': self.test_logo
			, 'category': 'LEN'
			, 'activities': [self.activity1.id]
		}
		# >1 activities
		data6 = {
			'name': 'Test6'
			, 'logo': self.test_logo
			, 'category': 'DIF'
			, 'activities': [self.activity1.id, self.activity2.id]
		}

		"""
		#FAILED: Try making request and enforcing CSRF validation
		factory = APIRequestFactory(enforce_csrf_checks=True)
		view = TagViewSet.as_view({'post':'create'})
		request4 = factory.post(self.url, data4, format='multipart')
		response4 = view(request4)
		"""

		response4 = self.client.post(self.url, data4, format='multipart') 
		response5 = self.client.post(self.url, data5, format='multipart')
		response6 = self.client.post(self.url, data6, format='multipart')

		#TODO self.assertEqual(response4.status_code, status.HTTP_201_CREATED)
		#TODO self.assertEqual(response5.status_code, status.HTTP_201_CREATED)
		#TODO self.assertEqual(response6.status_code, status.HTTP_201_CREATED)

		# API should include new resource ID number in response
		data4['id'] = 4
		data5['id'] = 5
		data6['id'] = 6

		#TODO self.assertEqual(response4.data, data4)
		#TODO self.assertEqual(response5.data, data5)
		#TODO self.assertEqual(response6.data, data6)

	def test_create_tag_invalid_data(self):
		"""
		Should NOT be able to create a new tag object with invalid data.
		"""

		# name missing
		data4 = {
			'name': ''
			, 'logo': self.test_logo
			, 'category': 'LAN'
			, 'activities': [self.activity1.id]
		}
		# logo missing
		data5 = {
			'name': 'Test5'
			, 'logo': ''
			, 'category': 'CON'
			, 'activities': []
		}
		# logo not an image
		data6 = {
			'name': 'Test6'
			, 'logo': 'TODO'
			, 'category': 'LAN'
			, 'activities': [self.activity2.id]
		}
		# logo filepath incorrect
		data7 = {
			'name': 'Test7'
			, 'logo': 'TODO'
			, 'category': 'LEN'
			, 'activities': []
		}
		# category missing
		data8 = {
			'name': 'Test8'
			, 'logo': self.test_logo
			, 'category': ''
			, 'activities': []
		}
		# category DNE
		data9 = {
			'name': 'Test9'
			, 'logo': self.test_logo
			, 'category': 'DNE'
			, 'activities': [self.activity1.id, self.activity2.id]
		}
		# activity DNE
		data10 = {
			'name': 'Test10'
			, 'logo': self.test_logo
			, 'category': 'DIF'
			, 'activities': [100]
		}

		response4 = self.client.post(self.url, data4, format='multipart')
		#TODO response5 = self.client.post(self.url, data5, format='multipart')
		#TODO response6 = self.client.post(self.url, data6, format='multipart')
		#TODO response7 = self.client.post(self.url, data7, format='multipart')
		response8 = self.client.post(self.url, data8, format='multipart')
		response9 = self.client.post(self.url, data9, format='multipart')
		response10 = self.client.post(self.url, data10, format='multipart')

		self.assertEqual(response4.status_code, status.HTTP_400_BAD_REQUEST)
		#TODO self.assertEqual(response5.status_code, status.HTTP_400_BAD_REQUEST)
		#TODO self.assertEqual(response6.status_code, status.HTTP_400_BAD_REQUEST)
		#TODO self.assertEqual(response7.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response8.status_code, status.HTTP_400_BAD_REQUEST)
		# Objects DNE, so should return 404 not found
		#TODO self.assertEqual(response9.status_code, status.HTTP_404_NOT_FOUND)
		#TODO self.assertEqual(response10.status_code, status.HTTP_404_NOT_FOUND)

		# API should include new resource ID number in response
		data4['id'] = 4
		data5['id'] = 5
		data6['id'] = 6
		data7['id'] = 7
		data8['id'] = 8
		data9['id'] = 9
		data10['id'] = 10

		#TODO self.assertEqual(response4.data, {'name': ['This field may not be blank.']})
		#TODO self.assertEqual(response5.data, {'url': ['This field may not be blank.']})
		#TODO self.assertEqual(response6.data, {'url': ['Enter a valid URL.']})
		#TODO self.assertEqual(response7.data, {'url': ['Enter a valid URL.']})
		#TODO self.assertEqual(response8.data, {'url': ['Enter a valid URL.']})
		#TODO self.assertEqual(response9.data, {'detail': 'Not found'})
		#TODO self.assertEqual(response10.data, {'detail': 'Not found'})

	def test_create_tag_duplicate_name(self):
		"""
		Should NOT be able to create a new tag object with duplicate value
		on unique-only field "name"
		"""

		# Duplicate name
		duplicate = {
			'name': 'Test1'
			, 'logo': self.test_logo
			, 'category': 'LAN'
			, 'activities': []
		}
	
		response = self.client.post(self.url, duplicate, format='multipart')

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		#TODO self.assertEqual(response.data, {'name': ['This field must be unique.']})

	""" TAG PATCH REQUESTS"""
	def test_update_tag(self):
		"""
		Should be able to update tag with PATCH request
		"""

		# Update name
		response1 = self.client.patch(self.url + "1/", {'name': 'Updated'}, format='json')
		data1 = {
			'id': 1
			, 'name': 'Updated'
			, 'logo': 'lessons/tests/test_img.jpg'
			, 'category': 'Language'
			, 'activities': []
		}
		
		# Update logo
		response2 = self.client.patch(self.url + "2/", {'logo': 'TODO'}, format='multipart')
		data2 = {
			'id': 2
			, 'name': 'Test2'
			, 'logo': 'TODO'
			, 'category': 'Technology'
			, 'activities': [self.activity1.id]
		}
		
		# Remove one activity
		response3 = self.client.patch(self.url + "3/", {'activities': [self.activity1.id]}, format='json')
		data3 = {
			'id': 3
			, 'name': 'Test3'
			, 'url': 'http://www.test3.com'
			, 'activities': [self.activity1.id]
		}

		# Remove all activities
		response4 = self.client.patch(self.url + "3/", {'activities': []}, format='json')
		data4 = {
			'id': 3
			, 'name': 'Test3'
			, 'url': 'http://www.test3.com'
			, 'activities': []
		}

		# Add first activity
		response5 = self.client.patch(
			url + "3/"
			, {'activities': [self.activity1.id]}
			, format='json'
		)
		data5 = {
			'id': 3
			, 'name': 'Test3'
			, 'url': 'http://www.test3.com'
			, 'activities': [self.activity1.id]
		}

		# Add additional activity
		response6 = self.client.patch(
			url + "3/"
			, {'activities': [self.activity1.id, self.activity2.id]}
			, format='json'
		)
		data6 = {
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

		self.assertEqual(response1.data, data1)
		self.assertEqual(response2.data, data2)
		self.assertEqual(response3.data, data3)
		self.assertEqual(response4.data, data4)
		self.assertEqual(response5.data, data5)
		self.assertEqual(response6.data, data6)
	
	def test_update_tag_invalid_data(self):
		"""
		Should NOT be able to update tag with PATCH request using invalid data
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

	def test_update_tag_that_DNE(self):
		"""
		Should NOT be able to update tag with PATCH request if it does not exist
		"""

		response = self.client.patch(self.url + "4/", {'name': 'Does not exist'}, format='json')

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(response.data, {'detail': 'Not found'})


	""" TAG DELETE REQUESTS """
	def test_delete_tag(self):
		"""
		Should be able to DELETE a tag object
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
		self.assertEqual(dict(response.data[0]), self.tag2)
		self.assertEqual(dict(response.data[1]), self.tag3)

	def test_delete_tag_that_DNE(self):
		"""
		Should NOT be able to DELETE a tag object that does not exist
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
		self.assertEqual(dict(response.data[0]), self.data1)
		self.assertEqual(dict(response.data[1]), self.data2)
		self.assertEqual(dict(response.data[2]), self.data3)

class ActivityTests(APITestCase):
	
	""" ACTIVITY TEST SETUP / TEARDOWN """

	@classmethod
	def setUpClass(cls):
		"""
		Fake objects to be used across all tests in this class
		"""
		# Endpoint URL for all tests
		cls.url = reverse('lessons:activity-list')

		# Create some tag objects to associate with activities
		test_logo = SimpleUploadedFile(
			name='test_img.jpg'
			, content=open('lessons/tests/test_img.jpg', 'r+b').read()
			, content_type='image/jpeg'
		)
		
		tag1 = Tag.objects.create(
			name='TestTag1'
			, logo=test_logo
			, category='LAN'
		)

		tag2 = Tag.objects.create(
			name='TestTag2'
			, logo=test_logo
			, category='TEC'
		)

		# Create some resource objects to associate with activities
		resource1 = Resource.objects.create(
			name='TestResource1'
			, url='http://www.testresource1.com'
		)
		resource2 = Resource.objects.create(
			name='TestResource2'
			, url='http://www.testresource2.com'
		)

		# Create some material objects to associate with activities
		material1 = Material.objects.create(
			name='TestMaterial1'
			, url='http://www.testmaterial1.com'
		)
		material2 = Material.objects.create(
			name='TestMaterial2'
			, url='http://www.testmaterial2.com'
		)

		# Create some curriculum objects to associate with activities
		curriculum1 = Curriculum.objects.create(
			name='TestCurriculum1'
			, description='This is a test curriculum.'
			, lower_grade=1
			, upper_grade=3
		)
		curriculum2 = Curriculum.objects.create(
			name='TestCurriculum2'
			, description='This is another test curriculum.'
			, lower_grade=2
			, upper_grade=4
		)

		# Add objects to the class object for reference in later tests
		cls.tag1 = tag1
		cls.tag2 = tag2
		cls.resource1 = resource1
		cls.resource2 = resource2
		cls.material1 = material1
		cls.material2 = material2
		cls.curriculum1 = curriculum1
		cls.curriculum2 = curriculum2

		# Create some activity objects
		activity1 = Activity.objects.create(
			name='Test1'
			, description="This is just a test activity."
			, teaching_notes ="This topic is very hard."
		)
		activity1.resources.add(resource1)
		activity1.materials.add(material1)
		activity1.materials.add(material2)

		activity2 = Activity.objects.create(
			name='Test2'
			, description="This is another test activity."
			, video_url='http://www.testactivity2.com'
		)
		activity2.tags.add(tag1)
		activity2.resources.add(resource1)
		activity2.resources.add(resource2)

		activity3 = Activity.objects.create(
			name='Test3'
			, description="This is the third test activity."
			, category='OFF'
		)
		activity3.tags.add(tag1, tag2)
		activity3.materials.add(material1)

		# Data to compare against objects returned from the API
		cls.activity1 = {
			'id': 1
			, 'name': 'Test1'
			, 'description': 'This is just a test activity.'
			, 'tags': []
			, 'category': ''
			, 'teaching_notes': ''
			, 'video_url': ''
			, 'image': None
			, 'get_curricula': []
			, 'relationships': []
			, 'materials': []
			, 'resources': []
		}
		cls.activity2 = {
			'id': 2
			, 'name': 'Test2'
			, 'description': 'This is another test activity.'
			, 'tags': []
			, 'category': ''
			, 'teaching_notes': ''
			, 'video_url': 'http://www.testactivity2.com'
			, 'image': None
			, 'get_curricula': []
			, 'relationships': []
			, 'materials': []
			, 'resources': []
		}
		cls.activity3 = {
			'id': 3
			, 'name': 'Test3'
			, 'description': "This is the third test activity."
			, 'tags': []
			, 'category': 'Offline'
			, 'teaching_notes': ''
			, 'video_url': ''
			, 'image': None
			, 'get_curricula': []
			, 'relationships': []
			, 'materials': []
			, 'resources': []
		}
	
	@classmethod
	def tearDownClass(cls):
		"""
		Delete objects
		"""
		Activity.objects.all().delete()

	""" ACTIVITY GET REQUESTS """
	def test_get_all_activities(self):
		"""
		Should be able to GET list of activities
		"""
		response = self.client.get(self.url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 3)

		# Convert ordered dict objects into unordered dicts for comparison
		self.assertEqual(dict(response.data[0]), self.activity1)
		self.assertEqual(dict(response.data[1]), self.activity2)
		self.assertEqual(dict(response.data[2]), self.activity3)

	def test_get_one_activity(self):
		"""
		Should be able to GET a single activity that exists
		"""
		response = self.client.get(self.url + "1/")

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# Convert ordered dict objects into unordered dicts for comparison
		self.assertEqual(response.data, self.activity1)

	def test_get_one_activity_that_DNE(self):
		"""
		Should fail to GET a single activity that does not exist
		"""
		response = self.client.get(self.url + "4/")

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		# Convert ordered dict objects into unordered dicts for comparison
		self.assertEqual(response.data, {'detail': 'Not found'})

	""" ACTIVITY POST REQUESTS """
	def test_create_activity(self):
		"""
		Should be able to create a new activity object with valid data.
		"""
		# 0 optional objects
		activity4 = {
			'name': 'Test4'
			, 'description': 'This is just a test activity.'
			, 'tag_IDs': [self.tag1.id]
			, 'category': ''
			, 'teaching_notes': ''
			, 'video_url': ''
			, 'curriculum_rels': []
			, 'relationships': []
			, 'material_IDs': []
			, 'resource_IDs': []
		}

		
		# 1 material
		activity5 = {
			'name': 'Test5'
			, 'description': 'This is just a test activity.'
			, 'tag_IDs': [self.tag2.id]
			, 'category': ''
			, 'teaching_notes': ''
			, 'video_url': ''
			, 'curriculum_rels': []
			, 'relationships': []
			, 'material_IDs': [self.material1.id]
			, 'resource_IDs': []
		}

		# 1 resource
		activity6 = {
			'name': 'Test6'
			, 'description': 'This is just a test activity.'
			, 'tag_IDs': [self.tag1.id]
			, 'category': ''
			, 'teaching_notes': ''
			, 'video_url': ''
			, 'curriculum_rels': []
			, 'relationships': []
			, 'material_IDs': []
			, 'resource_IDs': [self.resource1.id]
		}

		# 1 curriculum
		activity7 = {
			'name': 'Test7'
			, 'description': 'This is just a test activity.'
			, 'tag_IDs': [self.tag2.id]
			, 'category': ''
			, 'teaching_notes': ''
			, 'video_url': ''
			, 'curriculum_rels': [
				{
					"curriculumID": self.curriculum1.id
					, "number": 1
				}
			]
			, 'relationships': []
			, 'material_IDs': []
			, 'resource_IDs': []
		}

		"""
		# 1 activity relationship
		activity8 = {
			'name': 'Test8'
			, 'description': 'This is an additional test activity.'
			, 'tags': [self.tag1.id]
		}
		# TODO: multiple object relationships
		"""

		response4 = self.client.post(self.url, activity4, format='json')
		response5 = self.client.post(self.url, activity5, format='json')
		response6 = self.client.post(self.url, activity6, format='json')
		response7 = self.client.post(self.url, activity7, format='json')
		#response8 = self.client.post(self.url, activity8, format='json')

		self.assertEqual(response4.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response5.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response6.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response7.status_code, status.HTTP_201_CREATED)
		#self.assertEqual(response8.status_code, status.HTTP_201_CREATED)

		# API should include all info in response
		# ID numbers, image = None, nested objects
		activity4['id'] = 4
		activity4['image'] = None
		del(activity4['curriculum_rels'])
		activity4['get_curricula'] = []
		del(activity4['tag_IDs'])
		activity4['tags'] = [
			TagSerializer(self.tag1).data
		]
		del(activity4['material_IDs'])
		activity4['materials'] = []
		del(activity4['resource_IDs'])
		activity4['resources'] = []


		activity5['id'] = 5
		activity5['image'] = None
		del(activity5['curriculum_rels'])
		activity5['get_curricula'] = []
		del(activity5['tag_IDs'])
		activity5['tags'] = [
			TagSerializer(self.tag2).data
		]
		del(activity5['material_IDs'])
		activity5['materials'] = [MaterialSerializer(self.material1).data]
		del(activity5['resource_IDs'])
		activity5['resources'] = []


		activity6['id'] = 6
		activity6['image'] = None
		del(activity6['curriculum_rels'])
		activity6['get_curricula'] = []
		del(activity6['tag_IDs'])
		activity6['tags'] = [
			TagSerializer(self.tag1).data
		]
		del(activity6['material_IDs'])
		activity6['materials'] = []
		del(activity6['resource_IDs'])
		activity6['resources'] = [ResourceSerializer(self.resource1).data]


		activity7['id'] = 7
		activity7['image'] = None
		del(activity7['curriculum_rels'])
		activity7['get_curricula'] = [self.curriculum1.id]
		del(activity7['tag_IDs'])
		activity7['tags'] = [
			TagSerializer(self.tag2).data
		]
		del(activity7['material_IDs'])
		activity7['materials'] = []
		del(activity7['resource_IDs'])
		activity7['resources'] = []


		self.assertEqual(response4.data, activity4)
		self.assertEqual(response5.data, activity5)
		self.assertEqual(response6.data, activity6)
		self.assertEqual(response7.data, activity7)
		#self.assertEqual(response8.data, activity8)

	def test_create_activity_invalid_data(self):
		"""
		Should NOT be able to create a new activity object with invalid data.
		"""
		# name missing
		activity4 = {
			'name': ''
			, 'url': 'http://www.test4.com'
			, 'activities': [self.activity1.id]
		}
		# URL missing
		activity5 = {
			'name': 'Test5'
			, 'url': ''
			, 'activities': []
		}
		# URL malformed
		activity6 = {
			'name': 'Test6'
			, 'url': 'www.test6.com'
			, 'activities': [self.activity2.id]
		}
		# URL malformed
		activity7 = {
			'name': 'Test7'
			, 'url': 'test7.com'
			, 'activities': []
		}
		# URL malformed
		activity8 = {
			'name': 'Test8'
			, 'url': 'test8.co'
			, 'activities': []
		}
		# Activity DNE
		activity9 = {
			'name': 'Test9'
			, 'url': 'http://www.test9.com'
			, 'activities': [100]
		}

		response4 = self.client.post(self.url, activity4, format='json')
		response5 = self.client.post(self.url, activity5, format='json')
		response6 = self.client.post(self.url, activity6, format='json')
		response7 = self.client.post(self.url, activity7, format='json')
		response8 = self.client.post(self.url, activity8, format='json')
		response9 = self.client.post(self.url, activity9, format='json')

		self.assertEqual(response4.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response5.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response6.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response7.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response8.status_code, status.HTTP_400_BAD_REQUEST)
		# Activity DNE, so should return 404 not found
		self.assertEqual(response9.status_code, status.HTTP_404_NOT_FOUND)

		# API should include new activity ID number in response
		activity4['id'] = 4
		activity5['id'] = 5
		activity6['id'] = 6
		activity7['id'] = 7
		activity8['id'] = 8
		activity9['id'] = 9

		self.assertEqual(response4.data, {'name': ['This field may not be blank.']})
		self.assertEqual(response5.data, {'url': ['This field may not be blank.']})
		self.assertEqual(response6.data, {'url': ['Enter a valid URL.']})
		self.assertEqual(response7.data, {'url': ['Enter a valid URL.']})
		self.assertEqual(response8.data, {'url': ['Enter a valid URL.']})
		self.assertEqual(response9.data, {'detail': 'Not found'})

	def test_create_activity_duplicate_name(self):
		"""
		Should NOT be able to create a new activity object with duplicate value
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

	""" ACTIVITY PATCH REQUESTS"""
	def test_update_activity(self):
		"""
		Should be able to update activity with PATCH request
		"""

		# Update name
		response1 = self.client.patch(self.url + "1/", {'name': 'Updated'}, format='json')
		activity1 = {
			'id': 1
			, 'name': 'Updated'
			, 'url': 'http://www.test1.com'
			, 'activities': []
		}
		
		# Update URL
		response2 = self.client.patch(self.url + "2/", {'url': 'http://www.updated.com'}, format='json')
		activity2 = {
			'id': 2
			, 'name': 'Test2'
			, 'url': 'http://www.updated.com'
			, 'activities': [self.activity1.id]
		}
		
		# Remove one activity
		response3 = self.client.patch(self.url + "3/", {'activities': [self.activity1.id]}, format='json')
		activity3 = {
			'id': 3
			, 'name': 'Test3'
			, 'url': 'http://www.test3.com'
			, 'activities': [self.activity1.id]
		}

		# Remove all activities
		response4 = self.client.patch(self.url + "3/", {'activities': []}, format='json')
		activity4 = {
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
		activity5 = {
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
		activity6 = {
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

		self.assertEqual(response1.data, activity1)
		self.assertEqual(response2.data, activity2)
		self.assertEqual(response3.data, activity3)
		self.assertEqual(response4.data, activity4)
		self.assertEqual(response5.data, activity5)
		self.assertEqual(response6.data, activity6)
	
	def test_update_activity_invalid_data(self):
		"""
		Should NOT be able to update activity with PATCH request using invalid data
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

	def test_update_activity_that_DNE(self):
		"""
		Should NOT be able to update activity with PATCH request if it does not exist
		"""

		response = self.client.patch(self.url + "4/", {'name': 'Does not exist'}, format='json')

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(response.data, {'detail': 'Not found'})


	""" ACTIVITY DELETE REQUESTS """
	def test_delete_activity(self):
		"""
		Should be able to DELETE a activity object
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
		self.assertEqual(dict(response.data[0]), self.activity2)
		self.assertEqual(dict(response.data[1]), self.activity3)

	def test_delete_activity_that_DNE(self):
		"""
		Should NOT be able to DELETE a activity object that does not exist
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
		self.assertEqual(dict(response.data[0]), self.activity1)
		self.assertEqual(dict(response.data[1]), self.activity2)
		self.assertEqual(dict(response.data[2]), self.activity3)

	""" TODO: ACTIVITY-CURRICULUM RELATIONSHIPS """
	""" TODO: ACTIVITY-ACTIVITY RELATIONSHIPS """