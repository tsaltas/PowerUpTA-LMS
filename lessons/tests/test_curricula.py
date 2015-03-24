import unittest
import copy

from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from lessons.models import Activity, Curriculum, Material, Resource, Tag
from lessons.serializers import ActivitySerializer, MaterialSerializer, ResourceSerializer, TagSerializer

# for image mocking
from django.core.files.uploadedfile import SimpleUploadedFile
from mock import MagicMock
from django.core.files import File

class CurriculumTests(APITestCase):
	
	""" Curriculum TEST SETUP / TEARDOWN """

	@classmethod
	def setUpClass(cls):
		"""
		Fake objects to be used across all tests in this class
		"""
		pass
	
	@classmethod
	def tearDownClass(cls):
		"""
		Delete objects
		"""
		pass

	""" CURRICULUM GET REQUESTS """
	def test_get_all_curricula(self):
		"""
		Should be able to GET list of curricula
		"""
		pass

	def test_get_one_curriulum(self):
		"""
		Should be able to GET a single curriculum that exists
		"""
		pass

	def test_get_one_curriculum_that_DNE(self):
		"""
		Should fail to GET a single curriculum that does not exist
		"""
		pass

	""" CURRICULUM POST REQUESTS """
	def test_create_curriculum(self):
		"""
		Should be able to create a new curriculum object with valid data.
		"""
		pass

	def test_create_curriculum_missing_fields(self):
		"""
		Should NOT be able to create a new curriculum object with required fields missing
		"""
		
	def test_create_curriculum_invalid_data(self):
		"""
		Should NOT be able to create a new curriculum object with invalid data
		"""
	
	def test_add_activity_curriculum(self):
		"""
		Should be able to create curriculum-activity relationships with real activities
		"""
		pass

	def test_add_invalid_activity_curiculum(self):
		"""
		Should be able to create curriculum-activity relationships with invalid activities
		"""

#STOPPED HERE


	""" CURRICULUM PATCH REQUESTS """
	def test_update_activity(self):
		"""
		Should be able to update activity with PATCH request
		"""
		activity1 = {
			'id': 1
			, 'name': 'TestActivity1'
			, 'description': 'This is just a test activity.'
			, 'tags': []
			, 'category': ''
			, 'teaching_notes': 'This topic is very hard.'
			, 'video_url': ''
			, 'image': None
			, 'get_curricula': []
			, 'get_relationships': []
			, 'materials': [
				MaterialSerializer(self.material1).data
				, MaterialSerializer(self.material2).data
			]
			, 'resources': [
				ResourceSerializer(self.resource1).data
			]
		}

		# Update name
		response = self.client.patch(self.url + "1/", {'name': 'Updated'}, format='json')
		activity1['name'] = 'Updated'
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, activity1)

		# Update description
		response = self.client.patch(self.url + "1/", {'description': 'Updated description'}, format='json')
		activity1['description'] = 'Updated description'
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, activity1)

		# Add category
		response = self.client.patch(self.url + "1/", {'category': 'OFF'}, format='json')
		activity1['category'] = 'Offline'
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, activity1)

		# Update category
		response = self.client.patch(self.url + "1/", {'category': 'ONL'}, format='json')
		activity1['category'] = 'Online'
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, activity1)

		# Add video URL
		response = self.client.patch(self.url + "1/", {'video_url': 'http://www.video.com'}, format='json')
		activity1['video_url'] = 'http://www.video.com'
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, activity1)

		# Update video URL
		response = self.client.patch(self.url + "1/", {'video_url': 'http://www.updated.com'}, format='json')
		activity1['video_url'] = 'http://www.updated.com'
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, activity1)

		# Add some tags
		response = self.client.patch(self.url + "1/", {'tag_IDs': [self.tag1.id, self.tag2.id]}, format='json')
		activity1['tags'] = [TagSerializer(self.tag1).data, TagSerializer(self.tag2).data]
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, activity1)

		# Change the resource
		response = self.client.patch(self.url + "1/", {'resource_IDs': [self.resource2.id]}, format='json')
		activity1['resources'] = [ResourceSerializer(self.resource2).data]
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, activity1)

		# Delete all materials
		response = self.client.patch(self.url + "1/", {'material_IDs': []}, format='json')
		activity1['materials'] = []
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, activity1)

		# Add activity relationship
		response = self.client.patch(
			self.url + "1/"
			, {
				'activity_rels': [{
					"activityID": 2
					, "type": 'EXT'
					}]
			}
			, format='json'
		)
		activity1['get_relationships'] = [(2, 'extension')]
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, activity1)

		# Add curriculum relationship
		response = self.client.patch(
			self.url + "1/"
			, {
				'curriculum_rels': [{
					"curriculumID": self.curriculum1.id
					, "number": 2
					}]
			}
			, format='json'
		)
		activity1['get_curricula'] = [self.curriculum1.id]
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, activity1)

		# Delete activity and curriculum relationships
		response = self.client.patch(self.url + "1/", {'curriculum_rels': [], 'activity_rels': []}, format='json')
		activity1['get_relationships'] = []
		activity1['get_curricula'] = []
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, activity1)
	
	def test_update_activity_invalid_data(self):
		"""
		Should NOT be able to update activity with PATCH request using invalid data
		"""
		# Blank name
		response = self.client.patch(self.url + "1/", {'name': ''}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response.data, {'name': ["This field may not be blank."]})
		response = self.client.get(self.url + "1/")
		self.assertEqual(response.data, self.activity1)

		# Blank description
		response = self.client.patch(self.url + "1/", {'description': ''}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response.data, {'description': ["This field may not be blank."]})
		response = self.client.get(self.url + "1/")
		self.assertEqual(response.data, self.activity1)

		# Tag DNE
		response = self.client.patch(self.url + "1/", {'tag_IDs': [100]}, format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(response.data, {'detail': "Not found"})
		response = self.client.get(self.url + "1/")
		self.assertEqual(response.data, self.activity1)

		# Invalid category
		response = self.client.patch(self.url + "1/", {'category': 'DNE'}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response.data, {'category': ["`DNE` is not a valid choice."]})
		response = self.client.get(self.url + "1/")
		self.assertEqual(response.data, self.activity1)
		
		# Invalid video URL
		response = self.client.patch(self.url + "1/", {'video_url': 'cool.com'}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response.data, {'video_url': ["Enter a valid URL."]})
		response = self.client.get(self.url + "1/")
		self.assertEqual(response.data, self.activity1)
		
		# Curriculum DNE
		response = self.client.patch(
			self.url + "1/"
			, {
				'curriculum_rels': [{
					"curriculumID": 100
					, "number": 2
					}]
			}
			, format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(response.data, {'detail': "Not found"})
		response = self.client.get(self.url + "1/")
		self.assertEqual(response.data, self.activity1)
		
		# Activity DNE
		response = self.client.patch(
			self.url + "1/"
			, {
				'activity_rels': [{
					"activityID": 100
					, "type": 'EXT'
					}]
			}
			, format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(response.data, {'detail': "Not found"})
		response = self.client.get(self.url + "1/")
		self.assertEqual(response.data, self.activity1)

		"""
		# TODO: Invalid relationship type
		response = self.client.patch(
			self.url + "1/"
			, {
				'activity_rels': [{
					"activityID": self.activity2['id']
					, "type": 'DNE'
					}]
			}
			, format='json'
		)
		print response.data
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST
		self.assertEqual(response.data, {'detail': "Not found"})
		response = self.client.get(self.url + "1/")

		self.assertEqual(response.data, self.activity1)
		"""
		
		# Material DNE
		response = self.client.patch(self.url + "1/", {'material_IDs': [100]}, format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(response.data, {'detail': "Not found"})
		response = self.client.get(self.url + "1/")
		# Failed request removes old materials and does not add the invalid new one
		self.activity1["materials"] = []
		self.assertEqual(response.data, self.activity1)

		# Resource DNE
		response = self.client.patch(self.url + "1/", {'resource_IDs': [100]}, format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(response.data, {'detail': "Not found"})
		response = self.client.get(self.url + "1/")
		# Failed request removes old materials and does not add the invalid new one
		self.activity1["resources"] = []
		self.assertEqual(response.data, self.activity1)

	def test_update_activity_that_DNE(self):
		"""
		Should NOT be able to update activity with PATCH request if it does not exist
		"""
		response = self.client.patch(self.url + "4/", {'name': 'Does not exist'})

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

		# Remove ID of activity1 from resource on activity2
		activity2 = copy.deepcopy(self.activity2)
		del(activity2["resources"][0]["activities"][0])
		# Remove ID of activity1 from material on activity3
		activity3 = copy.deepcopy(self.activity3)
		del(activity3["materials"][0]["activities"][0])

		# Convert ordered dict objects into unordered dicts for comparison
		self.assertEqual(dict(response.data[0]), activity2)
		self.assertEqual(dict(response.data[1]), activity3)

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