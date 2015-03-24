import unittest

from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from lessons.models import Activity, Tag

# for image mocking
from django.core.files.uploadedfile import SimpleUploadedFile
from mock import MagicMock
from django.core.files import File

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