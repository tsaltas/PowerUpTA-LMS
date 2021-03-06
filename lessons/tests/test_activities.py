import copy

from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from lessons.models import Activity, Curriculum, Material, Resource, Tag
from lessons.serializers import MaterialSerializer, ResourceSerializer, TagSerializer

# for image mocking
from django.core.files.uploadedfile import SimpleUploadedFile


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
            , category='Language'
        )

        tag2 = Tag.objects.create(
            name='TestTag2'
            , logo=test_logo
            , category='Technology'
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
            name='TestActivity1'
            , description="This is just a test activity."
            , teaching_notes="This topic is very hard."
        )
        activity1.resources.add(resource1)
        activity1.materials.add(material1)
        activity1.materials.add(material2)

        activity2 = Activity.objects.create(
            name='TestActivity2'
            , description="This is another test activity."
            , video_url='http://www.testactivity2.com'
        )
        activity2.resources.add(resource1)
        activity2.resources.add(resource2)

        activity3 = Activity.objects.create(
            name='TestActivity3'
            , description="This is the third test activity."
            , category='Offline'
        )
        activity3.materials.add(material1)

        # Data to compare against objects returned from the API
        cls.activity1 = {
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
                MaterialSerializer(material1).data
                , MaterialSerializer(material2).data
            ]
            , 'resources': [
                ResourceSerializer(resource1).data
            ]
            , 'steps': []
        }
        cls.activity2 = {
            'id': 2
            , 'name': 'TestActivity2'
            , 'description': 'This is another test activity.'
            , 'tags': []
            , 'category': ''
            , 'teaching_notes': ''
            , 'video_url': 'http://www.testactivity2.com'
            , 'image': None
            , 'get_curricula': []
            , 'get_relationships': []
            , 'materials': []
            , 'resources': [
                ResourceSerializer(resource1).data
                , ResourceSerializer(resource2).data
            ]
            , 'steps': []
        }
        cls.activity3 = {
            'id': 3
            , 'name': 'TestActivity3'
            , 'description': "This is the third test activity."
            , 'tags': []
            , 'category': 'Offline'
            , 'teaching_notes': ''
            , 'video_url': ''
            , 'image': None
            , 'get_curricula': []
            , 'get_relationships': []
            , 'materials': [
                MaterialSerializer(material1).data
            ]
            , 'resources': []
            , 'steps': []
        }

    @classmethod
    def tearDownClass(cls):
        """
        Delete objects
        """
        Activity.objects.all().delete()
        Tag.objects.all().delete()
        Resource.objects.all().delete()
        Material.objects.all().delete()
        Curriculum.objects.all().delete()

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
        # TODO: Made description optional but did not write tests
        # TODO: Test "steps" relationships

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
            , 'category': 'Offline'
            , 'teaching_notes': 'This is hard to teach.'
            , 'video_url': 'http://www.test5.com'
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
            , 'category': 'Online'
            , 'teaching_notes': 'This is easy to teach.'
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
            , 'category': 'Discussion'
            , 'teaching_notes': 'Students should work at their own pace.'
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

        # 2 of each optional object
        activity8 = {
            'name': 'Test8'
            , 'description': 'This is just a loaded test activity.'
            , 'tag_IDs': [self.tag1.id, self.tag2.id]
            , 'category': 'Extension'
            , 'teaching_notes': ''
            , 'video_url': 'http://www.test8.com'
            , 'curriculum_rels': [
                {
                    "curriculumID": self.curriculum1.id
                    , "number": 2
                }
                , {
                    "curriculumID": self.curriculum2.id
                    , "number": 1
                }
            ]
            , 'activity_rels': []
            , 'material_IDs': [self.material1.id, self.material2.id]
            , 'resource_IDs': [self.resource1.id, self.resource2.id]
        }

        response4 = self.client.post(self.url, activity4)
        response5 = self.client.post(self.url, activity5)
        response6 = self.client.post(self.url, activity6)
        response7 = self.client.post(self.url, activity7)

        self.assertEqual(response4.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response5.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response6.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response7.status_code, status.HTTP_201_CREATED)

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
        activity4['steps'] = []

        activity5['id'] = 5
        activity5['image'] = None
        activity5['category'] = 'Offline'
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
        activity5['steps'] = []

        activity6['id'] = 6
        activity6['image'] = None
        activity6['category'] = 'Online'
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
        activity6['steps'] = []

        activity7['id'] = 7
        activity7['image'] = None
        activity7['category'] = 'Discussion'
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
        activity7['steps'] = []

        self.assertEqual(response4.data, activity4)
        self.assertEqual(response5.data, activity5)
        self.assertEqual(response6.data, activity6)
        self.assertEqual(response7.data, activity7)

        # Add last to avoid adding new activities to nested objects
        response8 = self.client.post(self.url, activity8)

        activity8['id'] = 8
        activity8['image'] = None
        activity8['category'] = 'Extension'
        del(activity8['curriculum_rels'])
        activity8['get_curricula'] = [self.curriculum1.id, self.curriculum2.id]
        del(activity8['tag_IDs'])
        activity8['tags'] = [
            TagSerializer(self.tag1).data
            , TagSerializer(self.tag2).data
        ]
        del(activity8['material_IDs'])
        activity8['materials'] = [
            MaterialSerializer(self.material1).data
            , MaterialSerializer(self.material2).data
        ]
        del(activity8['resource_IDs'])
        activity8['resources'] = [
            ResourceSerializer(self.resource1).data
            , ResourceSerializer(self.resource2).data
        ]
        del(activity8['activity_rels'])
        activity8['get_relationships'] = []
        activity8['steps'] = []

        self.assertEqual(response8.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response8.data, activity8)

    def test_create_activity_activity_relationships(self):
        # Setup:
        # Activity 4 is an extension of Activity 5
        # Activity 6 is a sub-activity of Activity 5
        # Activity 5 is a super-activity of Activity 6

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
        response4 = self.client.post(self.url, activity4)

        activity5 = {
            'name': 'Test5'
            , 'description': 'This is another test activity.'
            , 'tag_IDs': [self.tag2.id]
            , 'category': ''
            , 'teaching_notes': ''
            , 'video_url': ''
            , 'curriculum_rels': []
            , 'activity_rels': [
                {
                    "activityID": response4.data['id']
                    , "type": 'EXT'
                }
            ]
            , 'material_IDs': []
            , 'resource_IDs': []
        }
        response5 = self.client.post(self.url, activity5)

        activity6 = {
            'name': 'Test6'
            , 'description': 'This is a test activity.'
            , 'tag_IDs': [self.tag1.id]
            , 'category': ''
            , 'teaching_notes': ''
            , 'video_url': ''
            , 'curriculum_rels': []
            , 'activity_rels': [
                {
                    "activityID": response5.data['id']
                    , "type": 'SUP'
                }
            ]
            , 'material_IDs': []
            , 'resource_IDs': []
        }
        response6 = self.client.post(self.url, activity6)

        # Check HTTP responses
        self.assertEqual(response4.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response5.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response6.status_code, status.HTTP_201_CREATED)

        # GET new activity5 after updating relationship with 6
        response5 = self.client.get(self.url + str(response5.data['id']) + "/")
        self.assertEqual(response5.status_code, status.HTTP_200_OK)
        # fix issue with tags returned from test server
        response5.data["tags"] = [TagSerializer(self.tag2).data]

        # API should include all info in response (including those left blank)
        activity4['id'] = response4.data['id']
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
        activity4['steps'] = []

        activity5['id'] = response5.data['id']
        activity5['image'] = None
        del(activity5['curriculum_rels'])
        activity5['get_curricula'] = []
        del(activity5['tag_IDs'])
        activity5['tags'] = [
            TagSerializer(self.tag2).data
        ]
        del(activity5['material_IDs'])
        activity5['materials'] = []
        del(activity5['resource_IDs'])
        activity5['resources'] = []
        del(activity5['activity_rels'])
        activity5['steps'] = []

        activity6['id'] = response6.data['id']
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
        activity6['resources'] = []
        del(activity6['activity_rels'])
        activity6['steps'] = []

        # Should NOT be a symmetric activity relationship between Activity 4 and Activity 5
        # Activity 4 is an extension of Activity 5

        # Should be a symmetric activity relationship between Activity 6 and Activity 5
        # Activity 6 is a sub-activity of Activity 5
        # Activity 5 is a super-activity of Activity 6

        activity4['get_relationships'] = []
        activity5['get_relationships'] = [(response4.data['id'], 'extension'), (response6.data['id'], 'sub-activity')]
        activity6['get_relationships'] = [(response5.data['id'], 'super-activity')]

        # Check that correct data was saved
        self.assertEqual(response4.data, activity4)
        self.assertEqual(response5.data, activity5)
        self.assertEqual(response6.data, activity6)

    def test_create_activity_missing_fields(self):
        """
        Should NOT be able to create a new activity object with required fields missing
        """
        # Name missing
        activity = {
            'name': ''
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
        response = self.client.post(self.url, activity)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'name': ['This field may not be blank.']})

        # Tag missing
        activity = {
            'name': 'TestActivity - Tag missing'
            , 'description': 'This is just a test.'
            , 'tag_IDs': []
            , 'category': ''
            , 'teaching_notes': ''
            , 'video_url': ''
            , 'curriculum_rels': []
            , 'activity_rels': []
            , 'material_IDs': []
            , 'resource_IDs': []
        }

        response = self.client.post(self.url, activity)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'tag_IDs': ['This field may not be blank.']})

        # Verify only 3 original objects in the DB
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_activity_invalid_data(self):
        """
        Should NOT be able to create a new activity object with invalid data
        """

        # Tag DNE
        activity = {
            'name': 'TestActivity - Tag DNE'
            , 'description': 'This is just a test.'
            , 'tag_IDs': [100]
            , 'category': ''
            , 'teaching_notes': ''
            , 'video_url': ''
            , 'curriculum_rels': []
            , 'activity_rels': []
            , 'material_IDs': []
            , 'resource_IDs': []
        }

        response = self.client.post(self.url, activity)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'Not found'})

        # Category invalid
        activity = {
            'name': 'TestActivity - Category invalid'
            , 'description': 'This is just a test.'
            , 'tag_IDs': [self.tag1.id]
            , 'category': 'DNE'
            , 'teaching_notes': ''
            , 'video_url': ''
            , 'curriculum_rels': []
            , 'activity_rels': []
            , 'material_IDs': []
            , 'resource_IDs': []
        }
        response = self.client.post(self.url, activity)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'category': ['`DNE` is not a valid choice.']})

        # Malformed video URL
        activity = {
            'name': 'TestActivity - Video URL invalid'
            , 'description': 'This is just a test.'
            , 'tag_IDs': [self.tag1.id]
            , 'category': ''
            , 'teaching_notes': ''
            , 'video_url': 'cool.com'
            , 'curriculum_rels': []
            , 'activity_rels': []
            , 'material_IDs': []
            , 'resource_IDs': []
        }
        response = self.client.post(self.url, activity)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'video_url': ['Enter a valid URL.']})

        # Verify only 3 original objects in the DB
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_activity_invalid_objects(self):
        """
        Should be able to create a new activity object if non-required objects are invalid
        """

        # Material DNE
        activity = {
            'name': 'TestActivity - Material DNE'
            , 'description': 'This is just a test.'
            , 'tag_IDs': [self.tag1.id]
            , 'category': ''
            , 'teaching_notes': ''
            , 'video_url': ''
            , 'curriculum_rels': []
            , 'activity_rels': []
            , 'material_IDs': [100]
            , 'resource_IDs': []
        }
        response = self.client.post(self.url, activity)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'Not found'})

        # Resource DNE
        activity = {
            'name': 'TestActivity - Resource DNE'
            , 'description': 'This is just a test.'
            , 'tag_IDs': [self.tag1.id]
            , 'category': ''
            , 'teaching_notes': ''
            , 'video_url': ''
            , 'curriculum_rels': []
            , 'activity_rels': []
            , 'material_IDs': []
            , 'resource_IDs': [100]
        }

        response = self.client.post(self.url, activity)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'Not found'})

        # Curriculum DNE
        activity = {
            'name': 'TestActivity - Curriculum DNE'
            , 'description': 'This is just a test.'
            , 'tag_IDs': [self.tag1.id]
            , 'category': ''
            , 'teaching_notes': ''
            , 'video_url': ''
            , 'curriculum_rels': [
                {
                    "curriculumID": 100
                    , "number": 1
                }
            ]
            , 'activity_rels': []
            , 'material_IDs': []
            , 'resource_IDs': []
        }

        response = self.client.post(self.url, activity)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'Not found'})

        # Activity DNE
        activity = {
            'name': 'TestActivity - Activity DNE'
            , 'description': 'This is just a test.'
            , 'tag_IDs': [self.tag1.id]
            , 'category': ''
            , 'teaching_notes': ''
            , 'video_url': ''
            , 'curriculum_rels': []
            , 'activity_rels': [
                {
                    "activityID": 100
                    , "type": 'EXT'
                }
            ]
            , 'material_IDs': []
            , 'resource_IDs': []
        }

        response = self.client.post(self.url, activity)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'Not found'})

        # All DNE
        activity = {
            'name': 'TestActivity - All Objects DNE'
            , 'description': 'This is just a test.'
            , 'tag_IDs': [self.tag1.id]
            , 'category': ''
            , 'teaching_notes': ''
            , 'video_url': ''
            , 'curriculum_rels': [
                {
                    "curriculumID": 100
                    , "number": 1
                }
            ]
            , 'activity_rels': [
                {
                    "activityID": 100
                    , "type": 'EXT'
                }
            ]
            , 'material_IDs': [100]
            , 'resource_IDs': [100]
        }

        response = self.client.post(self.url, activity)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'Not found'})

        # Verify 5 new objects added to DB
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 8)

    """ ACTIVITY PATCH REQUESTS """
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
            , 'steps': []
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
        response = self.client.patch(self.url + "1/", {'category': 'Offline'}, format='json')
        activity1['category'] = 'Offline'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, activity1)

        # Update category
        response = self.client.patch(self.url + "1/", {'category': 'Online'}, format='json')
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
