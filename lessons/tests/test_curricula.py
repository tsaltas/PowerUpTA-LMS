from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from lessons.models import Activity, Curriculum
from lessons.serializers import ActivitySerializer, CurriculumSerializer


class CurriculumTests(APITestCase):
    """ CURRICULUM TEST SETUP / TEARDOWN """

    @classmethod
    def setUpClass(cls):
        """
        Fake objects to be used across all tests in this class
        """
        # Endpoint URL for all tests
        cls.url = reverse('lessons:curriculum-list')

        # Create some activity objects to associate with curricula
        activity1 = Activity.objects.create(
            name='TestActivity1'
            , description="This is just a test activity."
            , teaching_notes="This topic is very hard."
        )

        activity2 = Activity.objects.create(
            name='TestActivity2'
            , description="This is another test activity."
            , teaching_notes="This topic is fun."
        )

        activity3 = Activity.objects.create(
            name='TestActivity3'
            , description="Yet another test activity."
            , teaching_notes="This topic is awesome."
        )

        # Data to compare against objects returned from the API
        cls.activity1 = activity1
        cls.activity2 = activity2
        cls.activity3 = activity3
        cls.activity1data = ActivitySerializer(activity1).data
        cls.activity2data = ActivitySerializer(activity2).data
        cls.activity3data = ActivitySerializer(activity3).data

        # Create some curriculum objects
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

        # Data to compare against objects returned from the API
        cls.curriculum1 = curriculum1
        cls.curriculum2 = curriculum2
        cls.curriculum1data = CurriculumSerializer(curriculum1).data
        cls.curriculum2data = CurriculumSerializer(curriculum2).data

    @classmethod
    def tearDownClass(cls):
        """
        Delete objects
        """
        Activity.objects.all().delete()
        Curriculum.objects.all().delete()

    """ CURRICULUM GET REQUESTS """
    def test_get_all_curricula(self):
        """
        Should be able to GET list of curricula
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Convert ordered dict objects into unordered dicts for comparison
        self.assertEqual(dict(response.data[0]), self.curriculum1data)
        self.assertEqual(dict(response.data[1]), self.curriculum2data)

    def test_get_one_curriulum(self):
        """
        Should be able to GET a single curriculum that exists
        """
        response = self.client.get(self.url + "1/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Convert ordered dict objects into unordered dicts for comparison
        self.assertEqual(response.data, self.curriculum1data)

    def test_get_one_curriculum_that_DNE(self):
        """
        Should fail to GET a single curriculum that does not exist
        """
        response = self.client.get(self.url + "3/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Convert ordered dict objects into unordered dicts for comparison
        self.assertEqual(response.data, {'detail': 'Not found'})

    """ CURRICULUM POST REQUESTS """
    def test_create_curriculum(self):
        """
        Should be able to create a new curriculum object with valid data.
        """
        # no optional objects
        curriculum3 = {
            'name': 'TestCurriculum3'
            , 'description': 'This is a test curriculum.'
            , 'lower_grade': 0
            , 'upper_grade': 3
            , 'activity_rels': []
        }

        # optional activity
        curriculum4 = {
            'name': 'TestCurriculum4'
            , 'description': 'This is another test curriculum.'
            , 'lower_grade': 1
            , 'upper_grade': 5
            , 'activity_rels': [
                {
                    'activityID': self.activity1.id
                    , 'number': 1
                }
            ]
        }

        # optional tagline
        curriculum5 = {
            'name': 'TestCurriculum5'
            , 'tagline': 'Testing out the tagline'
            , 'description': 'This is another test curriculum.'
            , 'lower_grade': 2
            , 'upper_grade': 4
            , 'activity_rels': []
        }

        # 2 optional activities and tagline
        curriculum6 = {
            'name': 'TestCurriculum6'
            , 'tagline': 'Testing out the tagline plus two activities.'
            , 'description': 'This is another test curriculum.'
            , 'lower_grade': 3
            , 'upper_grade': 6
            , 'activity_rels': [
                {
                    'activityID': self.activity2.id
                    , 'number': 1
                }
                , {
                    'activityID': self.activity3.id
                    , 'number': 2
                }
            ]
        }

        response3 = self.client.post(self.url, curriculum3)
        response4 = self.client.post(self.url, curriculum4)
        response5 = self.client.post(self.url, curriculum5)
        response6 = self.client.post(self.url, curriculum6)

        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response4.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response5.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response6.status_code, status.HTTP_201_CREATED)

        # Add ID
        curriculum3['id'] = 3
        curriculum4['id'] = 4
        curriculum5['id'] = 5
        curriculum6['id'] = 6
        # Add activity list
        del(curriculum3["activity_rels"])
        del(curriculum4["activity_rels"])
        del(curriculum5["activity_rels"])
        del(curriculum6["activity_rels"])
        curriculum3['activities'] = []
        curriculum4['activities'] = [ActivitySerializer(self.activity1).data]
        curriculum5['activities'] = []
        curriculum6['activities'] = [ActivitySerializer(self.activity2).data, ActivitySerializer(self.activity3).data]
        # Add tagline
        curriculum3['tagline'] = ""
        curriculum4['tagline'] = ""
        # Update 0 to K
        curriculum3['lower_grade'] = 'K'

        self.assertEqual(response3.data, curriculum3)
        self.assertEqual(response4.data, curriculum4)
        self.assertEqual(response5.data, curriculum5)
        self.assertEqual(response6.data, curriculum6)

    def test_create_curriculum_missing_fields(self):
        """
        Should NOT be able to create a new curriculum object with required fields missing
        """
        # Missing name
        curriculum3 = {
            'description': 'This curriculum is missing a name.'
            , 'lower_grade': 0
            , 'upper_grade': 3
            , 'activity_rels': []
        }
        # Missing description
        curriculum4 = {
            'name': 'TestCurriculum4 (Missing description)'
            , 'lower_grade': 0
            , 'upper_grade': 3
            , 'activity_rels': []
        }
        # Missing lower grade
        curriculum5 = {
            'name': 'TestCurriculum5'
            , 'description': 'This curriculum is missing a lower grade.'
            , 'upper_grade': 3
            , 'activity_rels': []
        }
        # Missing upper grade
        curriculum6 = {
            'name': 'TestCurriculum6'
            , 'description': 'This curriculum is missing an upper grade.'
            , 'lower_grade': 3
            , 'activity_rels': []
        }

        response3 = self.client.post(self.url, curriculum3)
        response4 = self.client.post(self.url, curriculum4)
        response5 = self.client.post(self.url, curriculum5)
        response6 = self.client.post(self.url, curriculum6)

        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response4.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response5.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response6.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response3.data, {'name': ["This field is required."]})
        self.assertEqual(response4.data, {'description': ["This field is required."]})
        self.assertEqual(response5.data, {'lower_grade': ["This field is required."]})
        self.assertEqual(response6.data, {'upper_grade': ["This field is required."]})

    def test_create_curriculum_invalid_data(self):
        """
        Should NOT be able to create a new curriculum object with invalid data
        """
        # Blank name
        curriculum3 = {
            'name': ''
            , 'description': 'This curriculum has a blank name.'
            , 'lower_grade': 0
            , 'upper_grade': 3
            , 'activity_rels': []
        }
        # Blank description
        curriculum4 = {
            'name': 'TestCurriculum4 (Blank description)'
            , 'description': ''
            , 'lower_grade': 0
            , 'upper_grade': 3
            , 'activity_rels': []
        }
        # Empty string lower grade
        curriculum5 = {
            'name': 'TestCurriculum5'
            , 'description': 'This curriculum has an empty lower grade.'
            , 'lower_grade': ''
            , 'upper_grade': 3
            , 'activity_rels': []
        }
        # Null upper grade
        curriculum6 = {
            'name': 'TestCurriculum6'
            , 'description': 'This curriculum has a Null upper grade.'
            , 'lower_grade': 3
            , 'upper_grade': None
            , 'activity_rels': []
        }
        # Lower grade outside range
        curriculum7 = {
            'name': 'TestCurriculum7'
            , 'description': 'Lower grade outside range.'
            , 'lower_grade': -1
            , 'upper_grade': 3
            , 'activity_rels': []
        }
        # Upper grade outside range
        curriculum8 = {
            'name': 'TestCurriculum6'
            , 'description': 'Upper grade outside range.'
            , 'lower_grade': 3
            , 'upper_grade': 13
            , 'activity_rels': []
        }

        response3 = self.client.post(self.url, curriculum3)
        response4 = self.client.post(self.url, curriculum4)
        response5 = self.client.post(self.url, curriculum5)
        response6 = self.client.post(self.url, curriculum6)
        response7 = self.client.post(self.url, curriculum7)
        response8 = self.client.post(self.url, curriculum8)

        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response4.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response5.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response6.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response7.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response8.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response3.data, {'name': ["This field may not be blank."]})
        self.assertEqual(response4.data, {'description': ["This field may not be blank."]})
        self.assertEqual(response5.data, {'lower_grade': ["`` is not a valid choice."]})
        self.assertEqual(response6.data, {'upper_grade': ["This field may not be null."]})
        self.assertEqual(response7.data, {'lower_grade': ["`-1` is not a valid choice."]})
        self.assertEqual(response8.data, {'upper_grade': ["`13` is not a valid choice."]})

    def test_create_curriculum_invalid_activity(self):
        """
        Should NOT be able to create curriculum with invalid activity relationships
        """
        # Activity DNE
        curriculum3 = {
            'name': 'TestCurriculum3'
            , 'description': 'This curriculum has an invalid activity.'
            , 'lower_grade': 1
            , 'upper_grade': 3
            , 'activity_rels': [
                {
                    'activityID': 100
                    , 'number': 1
                }
            ]
        }
        response3 = self.client.post(self.url, curriculum3)
        self.assertEqual(response3.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response3.data, {'detail': 'Not found'})

        # One of several DNE
        curriculum4 = {
            'name': 'TestCurriculum4'
            , 'description': 'This curriculum has an invalid activity.'
            , 'lower_grade': 1
            , 'upper_grade': 3
            , 'activity_rels': [
                {
                    'activityID': self.activity1.id
                    , 'number': 1
                }
                , {
                    'activityID': 100
                    , 'number': 2
                }
            ]
        }
        response4 = self.client.post(self.url, curriculum4)
        self.assertEqual(response4.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response4.data, {'detail': 'Not found'})

    """ CURRICULUM PATCH REQUESTS """
    def test_update_curriculum(self):
        """
        Should be able to update curriculum with PATCH request
        """
        # Create a curriculum to update
        curriculum3 = {
            'name': 'OriginalName'
            , 'tagline': 'Original tagline.'
            , 'description': 'Original description.'
            , 'lower_grade': 1
            , 'upper_grade': 3
            , 'activity_rels': [
                {
                    'activityID': self.activity1.id
                    , 'number': 1
                }
            ]
        }
        # Add curriculum to database
        response3 = self.client.post(self.url, curriculum3)
        # Check object was created properly
        curriculum3['id'] = 9
        del(curriculum3["activity_rels"])
        curriculum3['activities'] = [ActivitySerializer(self.activity1).data]
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response3.data, curriculum3)

        # Update name
        response = self.client.patch(self.url + "9/", {'name': 'UpdatedName'})
        curriculum3['name'] = 'UpdatedName'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, curriculum3)
        # Update description
        response = self.client.patch(self.url + "9/", {'description': 'This description has been updated.'})
        curriculum3['description'] = 'This description has been updated.'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, curriculum3)
        # Update tagline
        response = self.client.patch(self.url + "9/", {'tagline': 'Updated tagline.'})
        curriculum3['tagline'] = 'Updated tagline.'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, curriculum3)
        # Update lower grade
        response = self.client.patch(self.url + "9/", {'lower_grade': 2})
        curriculum3['lower_grade'] = 2
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, curriculum3)
        # Update upper grade
        response = self.client.patch(self.url + "9/", {'upper_grade': 4})
        curriculum3['upper_grade'] = 4
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, curriculum3)

    def test_update_curriculum_that_DNE(self):
        """
        Should NOT be able to update curriculum with PATCH request if it does not exist
        """
        response = self.client.patch(self.url + "100/", {'name': 'Does not exist'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'Not found'})

    def test_update_curriculum_invalid_data(self):
        """
        Should NOT be able to update curriculum with PATCH request using invalid data
        """
        # Create a curriculum to update
        curriculum3 = {
            'name': 'OriginalName'
            , 'tagline': 'Original tagline.'
            , 'description': 'Original description.'
            , 'lower_grade': 1
            , 'upper_grade': 3
            , 'activity_rels': [
                {
                    'activityID': self.activity1.id
                    , 'number': 1
                }
            ]
        }
        # Add curriculum to database
        response3 = self.client.post(self.url, curriculum3)
        # Check object was created properly
        curriculum3['id'] = 11
        del(curriculum3["activity_rels"])
        curriculum3['activities'] = [ActivitySerializer(self.activity1).data]
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response3.data, curriculum3)

        # Blank name
        response = self.client.patch(self.url + "11/", {'name': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'name': ['This field may not be blank.']})
        response = self.client.get(self.url + "11/")
        self.assertEqual(response.data, curriculum3)

        # Null description
        response = self.client.patch(self.url + "11/", {'description': None})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'description': ['This field may not be null.']})
        response = self.client.get(self.url + "11/")
        self.assertEqual(response.data, curriculum3)

        # Update lower grade
        response = self.client.patch(self.url + "11/", {'lower_grade': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'lower_grade': ["`` is not a valid choice."]})
        response = self.client.get(self.url + "11/")
        self.assertEqual(response.data, curriculum3)

        # Null upper grade
        response = self.client.patch(self.url + "11/", {'upper_grade': None})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'upper_grade': ['This field may not be null.']})
        response = self.client.get(self.url + "11/")
        self.assertEqual(response.data, curriculum3)

        # Should be able to remove tagline
        response = self.client.patch(self.url + "11/", {'tagline': ''})
        curriculum3['tagline'] = ''
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, curriculum3)

    def test_update_curriculum_activities(self):
        """
        Should be able to add a valid activity to an existing curriculum with a PATCH request
        Should be able to remove an activity from a curriculum
        """
        # Create a curriculum to update
        curriculum3 = {
            'name': 'TestCurriculum3'
            , 'tagline': 'Optional tagline.'
            , 'description': 'This is a test curriculum.'
            , 'lower_grade': 1
            , 'upper_grade': 3
            , 'activity_rels': [
                {
                    'activityID': self.activity1.id
                    , 'number': 1
                }
            ]
        }
        # Add curriculum to database
        response3 = self.client.post(self.url, curriculum3)
        # Check object was created properly
        curriculum3['id'] = 10
        del(curriculum3["activity_rels"])
        curriculum3['activities'] = [ActivitySerializer(self.activity1).data]
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response3.data, curriculum3)

        # Add another activity
        response = self.client.patch(
            self.url + "10/"
            , {
                'activity_rels': [
                    {
                        'activityID': self.activity1.id
                        , 'number': 1
                    }
                    , {
                        'activityID': self.activity2.id
                        , 'number': 2
                    }
                ]
            }
        )
        curriculum3['activities'] = [ActivitySerializer(self.activity1).data, ActivitySerializer(self.activity2).data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, curriculum3)

        # Remove an activity
        response = self.client.patch(
            self.url + "10/"
            , {
                'activity_rels': [
                    {
                        'activityID': self.activity2.id
                        , 'number': 2
                    }
                ]
            }
        )
        curriculum3['activities'] = [ActivitySerializer(self.activity2).data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, curriculum3)

        # Remove all activities
        response = self.client.patch(
            self.url + "10/"
            , {'activity_rels': []}
        )
        curriculum3['activities'] = []
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, curriculum3)

    def test_add_invalid_activity_curriculum(self):
        """
        Should NOT be able to add invalid activity to an existing curriculum
        """
        response = self.client.patch(
            self.url + str(self.curriculum1.id) + "/"
            , {
                'activity_rels': [
                    {
                        'activityID': 100
                        , 'number': 1
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get(self.url + str(self.curriculum1.id) + "/")
        self.assertEqual(response.data, CurriculumSerializer(self.curriculum1).data)

    """ CURRICULUM DELETE REQUESTS """
    def test_delete_curriculum(self):
        """
        Should be able to DELETE a curriculum object
        """
        response = self.client.delete(self.url + "1/")

        # Verify object deletion
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

        # Verify that other object remains
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(dict(response.data[0]), CurriculumSerializer(self.curriculum2).data)

    def test_delete_curriculum_that_DNE(self):
        """
        Should NOT be able to DELETE a curriculum object that does not exist
        """
        response = self.client.delete(self.url + "4/")

        # Verify object deletion
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'Not found'})

        # Verify that all objects remain
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 2)
        self.assertEqual(dict(response.data[0]), CurriculumSerializer(self.curriculum1).data)
        self.assertEqual(dict(response.data[1]), CurriculumSerializer(self.curriculum2).data)
