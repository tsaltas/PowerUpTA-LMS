import json

from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from django.shortcuts import get_object_or_404

from rest_framework.test import APITestCase, APIRequestFactory

from rest_framework import status

from lessons.models import Activity, Material, Resource, Tag

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
			, 'activities': [activity1.id]
		}
		cls.data3 = {
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
		self.assertEqual(dict(response.data[0]), self.data1)
		self.assertEqual(dict(response.data[1]), self.data2)
		self.assertEqual(dict(response.data[2]), self.data3)

	def test_get_one_material(self):
		"""
		Should be able to GET a single material that exists
		"""
		response = self.client.get(self.url + "1/")

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# Convert ordered dict objects into unordered dicts for comparison
		self.assertEqual(response.data, self.data1)

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
		data4 = {
			'name': 'Test4'
			, 'url': 'http://www.test4.com'
			, 'activities': []
		}
		# 1 activity
		data5 = {
			'name': 'Test5'
			, 'url': 'http://www.test5.com'
			, 'activities': [self.activity1.id]
		}
		# >1 activities
		data6 = {
			'name': 'Test6'
			, 'url': 'http://www.test6.com'
			, 'activities': [self.activity1.id, self.activity2.id]
		}

		response4 = self.client.post(self.url, data4, format='json')
		response5 = self.client.post(self.url, data5, format='json')
		response6 = self.client.post(self.url, data6, format='json')

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
		# name missing
		data4 = {
			'name': ''
			, 'url': 'http://www.test4.com'
			, 'activities': [self.activity1.id]
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
			, 'activities': [self.activity2.id]
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
			, 'activities': [100]
		}

		response4 = self.client.post(self.url, data4, format='json')
		response5 = self.client.post(self.url, data5, format='json')
		response6 = self.client.post(self.url, data6, format='json')
		response7 = self.client.post(self.url, data7, format='json')
		response8 = self.client.post(self.url, data8, format='json')
		response9 = self.client.post(self.url, data9, format='json')

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
		data1 = {
			'id': 1
			, 'name': 'Updated'
			, 'url': 'http://www.test1.com'
			, 'activities': []
		}
		
		# Update URL
		response2 = self.client.patch(self.url + "2/", {'url': 'http://www.updated.com'}, format='json')
		data2 = {
			'id': 2
			, 'name': 'Test2'
			, 'url': 'http://www.updated.com'
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
			self.url + "3/"
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
			self.url + "3/"
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
		self.assertEqual(dict(response.data[0]), self.data2)
		self.assertEqual(dict(response.data[1]), self.data3)

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
		self.assertEqual(dict(response.data[0]), self.data1)
		self.assertEqual(dict(response.data[1]), self.data2)
		self.assertEqual(dict(response.data[2]), self.data3)

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

		# Create some resources objects
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
			, 'activities': [activity1.id]
		}
		cls.data3 = {
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
		self.assertEqual(dict(response.data[0]), self.data1)
		self.assertEqual(dict(response.data[1]), self.data2)
		self.assertEqual(dict(response.data[2]), self.data3)

	def test_get_one_resource(self):
		"""
		Should be able to GET a single resource that exists
		"""
		response = self.client.get(self.url + "1/")

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# Convert ordered dict objects into unordered dicts for comparison
		self.assertEqual(response.data, self.data1)

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
		data4 = {
			'name': 'Test4'
			, 'url': 'http://www.test4.com'
			, 'activities': []
		}
		# 1 activity
		data5 = {
			'name': 'Test5'
			, 'url': 'http://www.test5.com'
			, 'activities': [self.activity1.id]
		}
		# >1 activities
		data6 = {
			'name': 'Test6'
			, 'url': 'http://www.test6.com'
			, 'activities': [self.activity1.id, self.activity2.id]
		}

		response4 = self.client.post(self.url, data4, format='json')
		response5 = self.client.post(self.url, data5, format='json')
		response6 = self.client.post(self.url, data6, format='json')

		self.assertEqual(response4.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response5.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response6.status_code, status.HTTP_201_CREATED)

		# API should include new resource ID number in response
		data4['id'] = 4
		data5['id'] = 5
		data6['id'] = 6

		self.assertEqual(response4.data, data4)
		self.assertEqual(response5.data, data5)
		self.assertEqual(response6.data, data6)

	def test_create_resource_invalid_data(self):
		"""
		Should NOT be able to create a new resource object with invalid data.
		"""
		# name missing
		data4 = {
			'name': ''
			, 'url': 'http://www.test4.com'
			, 'activities': [self.activity1.id]
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
			, 'activities': [self.activity2.id]
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
			, 'activities': [100]
		}

		response4 = self.client.post(self.url, data4, format='json')
		response5 = self.client.post(self.url, data5, format='json')
		response6 = self.client.post(self.url, data6, format='json')
		response7 = self.client.post(self.url, data7, format='json')
		response8 = self.client.post(self.url, data8, format='json')
		response9 = self.client.post(self.url, data9, format='json')

		self.assertEqual(response4.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response5.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response6.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response7.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response8.status_code, status.HTTP_400_BAD_REQUEST)
		# Activity DNE, so should return 404 not found
		self.assertEqual(response9.status_code, status.HTTP_404_NOT_FOUND)

		# API should include new resource ID number in response
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
		data1 = {
			'id': 1
			, 'name': 'Updated'
			, 'url': 'http://www.test1.com'
			, 'activities': []
		}
		
		# Update URL
		response2 = self.client.patch(self.url + "2/", {'url': 'http://www.updated.com'}, format='json')
		data2 = {
			'id': 2
			, 'name': 'Test2'
			, 'url': 'http://www.updated.com'
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
			self.url + "3/"
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
			self.url + "3/"
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
		self.assertEqual(dict(response.data[0]), self.data2)
		self.assertEqual(dict(response.data[1]), self.data3)

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
		self.assertEqual(dict(response.data[0]), self.data1)
		self.assertEqual(dict(response.data[1]), self.data2)
		self.assertEqual(dict(response.data[2]), self.data3)

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
		test_logo = SimpleUploadedFile(
			name='test_img.jpg'
			, content=open('lessons/tests/test_img.jpg', 'rb').read()
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
		cls.data1 = {
			'id': 1
			, 'name': 'Test1'
			, 'logo': 'lessons/tests/test_img.jpg'
			, 'category': 'LAN'
			, 'activities': []
		}
		cls.data2 = {
			'id': 2
			, 'name': 'Test2'
			, 'logo': 'lessons/tests/test_img.jpg'
			, 'category': 'TEC'
			, 'activities': []
		}
		cls.data3 = {
			'id': 2
			, 'name': 'Test2'
			, 'logo': 'lessons/tests/test_img.jpg'
			, 'category': 'CON'
			, 'activities': []
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
			'name': 'Test4'
			, 'logo': 'lessons/tests/test_img.jpg'
			, 'category': 'LAN'
			, 'activities': []
		}
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

		response4 = self.client.post(self.url, data4)
		response5 = self.client.post(self.url, data5, format='json')
		response6 = self.client.post(self.url, data6, format='json')

		self.assertEqual(response4.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response5.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response6.status_code, status.HTTP_201_CREATED)

		# API should include new resource ID number in response
		data4['id'] = 4
		data5['id'] = 5
		data6['id'] = 6

		self.assertEqual(response4.data, data4)
		self.assertEqual(response5.data, data5)
		self.assertEqual(response6.data, data6)

	def test_create_tag_invalid_data(self):
		"""
		Should NOT be able to create a new tag object with invalid data.
		"""

		# name missing
		data4 = {
			'name': ''
			, 'logo': 'lessons/tests/test_img.jpg'
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
			, 'logo': 'lessons/tests/test_img.pdf'
			, 'category': 'LAN'
			, 'activities': [self.activity2.id]
		}
		# logo filepath incorrect
		data7 = {
			'name': 'Test7'
			, 'logo': 'tests/test_img.jpg'
			, 'category': 'LEN'
			, 'activities': []
		}
		# category missing
		data8 = {
			'name': 'Test8'
			, 'logo': 'lessons/tests/test_img.jpg'
			, 'category': ''
			, 'activities': []
		}
		# category DNE
		data9 = {
			'name': 'Test9'
			, 'logo': 'lessons/tests/test_img.jpg'
			, 'category': 'DNE'
			, 'activities': [self.activity1.id, self.activity2.id]
		}
		# activity DNE
		data10 = {
			'name': 'Test10'
			, 'logo': 'lessons/tests/test_img.jpg'
			, 'category': 'DIF'
			, 'activities': [100]
		}

		response4 = self.client.post(self.url, data4, format='json')
		response5 = self.client.post(self.url, data5, format='json')
		response6 = self.client.post(self.url, data6, format='json')
		response7 = self.client.post(self.url, data7, format='json')
		response8 = self.client.post(self.url, data8, format='json')
		response9 = self.client.post(self.url, data9, format='json')
		response10 = self.client.post(self.url, data10, format='json')

		self.assertEqual(response4.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response5.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response6.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response7.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response8.status_code, status.HTTP_400_BAD_REQUEST)
		# Objects DNE, so should return 404 not found
		self.assertEqual(response9.status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(response10.status_code, status.HTTP_404_NOT_FOUND)

		# API should include new resource ID number in response
		data4['id'] = 4
		data5['id'] = 5
		data6['id'] = 6
		data7['id'] = 7
		data8['id'] = 8
		data9['id'] = 9
		data10['id'] = 10

		self.assertEqual(response4.data, {'name': ['This field may not be blank.']})
		self.assertEqual(response5.data, {'url': ['This field may not be blank.']})
		self.assertEqual(response6.data, {'url': ['Enter a valid URL.']})
		self.assertEqual(response7.data, {'url': ['Enter a valid URL.']})
		self.assertEqual(response8.data, {'url': ['Enter a valid URL.']})
		self.assertEqual(response9.data, {'detail': 'Not found'})
		self.assertEqual(response10.data, {'detail': 'Not found'})

	def test_create_tag_duplicate_name(self):
		"""
		Should NOT be able to create a new tag object with duplicate value
		on unique-only field "name"
		"""

		# Duplicate name
		duplicate = {
			'name': 'Test1'
			, 'logo': 'lessons/tests/test_img.jpg'
			, 'category': 'LAN'
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
		data1 = {
			'id': 1
			, 'name': 'Updated'
			, 'url': 'http://www.test1.com'
			, 'activities': []
		}
		
		# Update URL
		response2 = self.client.patch(self.url + "2/", {'url': 'http://www.updated.com'}, format='json')
		data2 = {
			'id': 2
			, 'name': 'Test2'
			, 'url': 'http://www.updated.com'
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
		self.assertEqual(dict(response.data[0]), self.data2)
		self.assertEqual(dict(response.data[1]), self.data3)

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
		self.assertEqual(dict(response.data[0]), self.data1)
		self.assertEqual(dict(response.data[1]), self.data2)
		self.assertEqual(dict(response.data[2]), self.data3)