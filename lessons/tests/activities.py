import unittest

from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from lessons.models import Activity, Curriculum, Material, Resource, Tag
from lessons.serializers import ActivitySerializer, MaterialSerializer, ResourceSerializer, TagSerializer
from lessons.views import ActivityViewSet

# for image mocking
from django.core.files.uploadedfile import SimpleUploadedFile
from mock import MagicMock
from django.core.files import File

#@unittest.skip("Skip activity testing for now.")
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
		cls.activity1 = activity1
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
			, 'get_relationships': []
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
			, 'get_relationships': []
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
			, 'activity_rels': []
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
			, 'activity_rels': []
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
			, 'activity_rels': []
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
			, 'activity_rels': []
			, 'material_IDs': []
			, 'resource_IDs': []
		}

		# 1 activity relationship (Extension)
		activity8 = {
			'name': 'Test8'
			, 'description': 'This is just a test activity.'
			, 'tag_IDs': [self.tag1.id]
			, 'category': ''
			, 'teaching_notes': ''
			, 'video_url': ''
			, 'curriculum_rels': []
			, 'activity_rels': [
				{
					"activityID": self.activity1.id
					, "type": 'EXT'
				}
			]
			, 'material_IDs': []
			, 'resource_IDs': []
		}

		# TODO: test creatin activities with multiple object relationships
		# TODO: Make symmetric relatoinship for related activities

		response4 = self.client.post(self.url, activity4)
		response5 = self.client.post(self.url, activity5)
		response6 = self.client.post(self.url, activity6)
		response7 = self.client.post(self.url, activity7)
		response8 = self.client.post(self.url, activity8)

		self.assertEqual(response4.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response5.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response6.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response7.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response8.status_code, status.HTTP_201_CREATED)

		# API should include all info in response
		# ID numbers, image = None, nested objects are included, data for object creation should get deleted
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
		del(activity4['activity_rels'])
		activity4['get_relationships'] = []


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
		del(activity5['activity_rels'])
		activity5['get_relationships'] = []


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
		del(activity6['activity_rels'])
		activity6['get_relationships'] = []


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
		del(activity7['activity_rels'])
		activity7['get_relationships'] = []


		activity8['id'] = 8
		activity8['image'] = None
		del(activity8['curriculum_rels'])
		activity8['get_curricula'] = []
		del(activity8['tag_IDs'])
		activity8['tags'] = [
			TagSerializer(self.tag1).data
		]
		del(activity8['material_IDs'])
		activity8['materials'] = []
		del(activity8['resource_IDs'])
		activity8['resources'] = []
		del(activity8['activity_rels'])
		activity8['get_relationships'] = [
			(self.activity1.id, 'extension')
		]

		self.assertEqual(response4.data, activity4)
		self.assertEqual(response5.data, activity5)
		self.assertEqual(response6.data, activity6)
		self.assertEqual(response7.data, activity7)
		self.assertEqual(response8.data, activity8)

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