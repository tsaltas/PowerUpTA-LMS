from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from lessons.models import Activity, Material

from lessons.serializers import ActivitySerializer, MaterialSerializer


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

        # Data to compare in later tests
        cls.material1 = MaterialSerializer(material1).data
        cls.material2 = MaterialSerializer(material2).data
        cls.material3 = MaterialSerializer(material3).data
        cls.activity1 = ActivitySerializer(activity1).data
        cls.activity2 = ActivitySerializer(activity2).data

        # Add serialized objects to test DB
        client = APIClient()
        client.post(reverse('lessons:material-list'), cls.material1)
        client.post(reverse('lessons:material-list'), cls.material2)
        client.post(reverse('lessons:material-list'), cls.material3)
        client.post(reverse('lessons:activity-list'), cls.activity1)
        client.post(reverse('lessons:activity-list'), cls.activity2)

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
            , 'activities': [self.activity1["id"]]
        }
        # >1 activities
        material6 = {
            'name': 'Test6'
            , 'url': 'http://www.test6.com'
            , 'activities': [self.activity1["id"], self.activity2["id"]]
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
            , 'activities': [self.activity1["id"]]
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
            , 'activities': [self.activity2["id"]]
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
            , 'activities': [self.activity1["id"]]
        }

        # Remove one activity
        response3 = self.client.patch(self.url + "3/", {'activities': [self.activity1["id"]]}, format='json')
        material3 = {
            'id': 3
            , 'name': 'Test3'
            , 'url': 'http://www.test3.com'
            , 'activities': [self.activity1["id"]]
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
            , {'activities': [self.activity1["id"]]}
            , format='json'
        )
        material5 = {
            'id': 3
            , 'name': 'Test3'
            , 'url': 'http://www.test3.com'
            , 'activities': [self.activity1["id"]]
        }

        # Add additional activity
        response6 = self.client.patch(
            self.url + "3/"
            , {'activities': [self.activity1["id"], self.activity2["id"]]}
            , format='json'
        )
        material6 = {
            'id': 3
            , 'name': 'Test3'
            , 'url': 'http://www.test3.com'
            , 'activities': [self.activity1["id"], self.activity2["id"]]
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
