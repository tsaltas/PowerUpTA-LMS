import sys

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from lessons.models import Curriculum, Activity, Tag, Material, Resource, CurriculumActivityRelationship
from lessons.serializers import TagSerializer, MaterialSerializer, ActivitySerializer, ResourceSerializer, CurriculumSerializer, CurriculumActivityRelationshipSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response


class TagViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    # Custom function to associate activities with tag
    def create(self, request):
        print "CREATING NEW TAG!"
        # print "inside the creation function"
        # print "request content type: "
        # print request.content_type
        # print "request.data: "
        # print request.data
        # print "request.FILES: "
        # print request.FILES
        # print "test logo file size (inside views.py): " + str(request.data["logo"].size)

        serializer = TagSerializer(data=request.data)
        activities = []

        if 'activities' in request.data:
            activities = request.data["activities"]

        if serializer.is_valid():
            # print "serializer was valid!"
            # Save new tag instance and pass in list of activities to be associated with the tag
            serializer.save(activities=activities)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # print "serializer not valid"
            print serializer.errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Custom function to remove activities from tag if specified
    def partial_update(self, request, pk=None):
        # Get the tag object
        tag = get_object_or_404(Tag, pk=pk)

        # Get new activities list
        if 'activities' in request.data:
            activities = request.data["activities"]
        else:
            activities = [activity.id for activity in tag.activities.all()]

        # Update `tag` with partial data
        serializer = TagSerializer(tag, request.data, partial=True)
        if serializer.is_valid():
            serializer.save(activities=activities)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MaterialViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    # Custom function to associate activities with material
    def create(self, request):
        serializer = MaterialSerializer(data=request.data)

        if serializer.is_valid():
            # Save new material instance and pass in list of activities to be associated with the material
            serializer.save(activities=request.data['activities'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Custom function to remove activities from material if specified
    def partial_update(self, request, pk=None):
        # Get the material object
        material = get_object_or_404(Material, pk=pk)
        # Update `material` with partial data
        serializer = MaterialSerializer(material, request.data, partial=True)
        if serializer.is_valid():
            # Get new activities list if necessary
            if 'activities' in request.data:
                activities = request.data["activities"]
                serializer.save(activities=activities)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResourceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    # Custom function to associate activities with resource
    def create(self, request):
        serializer = ResourceSerializer(data=request.data)

        if serializer.is_valid():
            # Save new resource instance and pass in list of activities to be associated with the resource
            serializer.save(activities=request.data['activities'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Custom function to remove activities from resource if specified
    def partial_update(self, request, pk=None):
        # Get the resource object
        resource = get_object_or_404(Resource, pk=pk)
        # Update `resource` with partial data
        serializer = ResourceSerializer(resource, request.data, partial=True)

        if serializer.is_valid():
            # Get new activities list if necessary
            if 'activities' in request.data:
                activities = request.data["activities"]
                serializer.save(activities=activities)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    # Custom function to associate activities with resources, materials, tags, curricula, and other activities
    def create(self, request):
        serializer = ActivitySerializer(data=request.data)

        if serializer.is_valid():
            # If no tag_IDs, return 400_BAD_REQUEST
            if (("tag_IDs" not in request.data) or (len(request.data["tag_IDs"]) == 0)):
                return Response({'tag_IDs': ['This field may not be blank.']}, status=status.HTTP_400_BAD_REQUEST)
            # If any tag_ID is invalid, return 404_NOT_FOUND
            for tagID in request.data["tag_IDs"]:
                try:
                    Tag.objects.get(pk=tagID)
                except ObjectDoesNotExist:
                    return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

            # Look for errors with any curricula and activities passed in
            rel_errors = 0
            curriculum_rels = []
            activity_rels = []
            material_IDs = []
            resource_IDs = []

            if "material_IDs" in request.data:
                material_IDs = request.data["material_IDs"]
            if "resource_IDs" in request.data:
                resource_IDs = request.data["resource_IDs"]

            if "curriculum_rels" in request.data:
                curricula = request.data["curriculum_rels"]
                for rel in curricula:
                    try:
                        Curriculum.objects.get(pk=rel["curriculumID"])
                        curriculum_rels.append(rel)
                    except ObjectDoesNotExist:
                        rel_errors += 1

            if "activity_rels" in request.data:
                activities = request.data["activity_rels"]
                for rel in activities:
                    try:
                        Activity.objects.get(pk=rel["activityID"])
                        activity_rels.append(rel)
                    except ObjectDoesNotExist:
                        rel_errors += 1
            # Save new activity instance and pass in lists of objects to be associated with the activity
            serializer.save(
                tag_IDs=request.data["tag_IDs"]
                , curriculum_rels=curriculum_rels
                , material_IDs=material_IDs
                , resource_IDs=resource_IDs
                , activity_rels=activity_rels
            )

            if (rel_errors > 0):
                return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Custom function to manage objects related to activity on patch / update request
    def partial_update(self, request, pk=None):
        # Get the activity object
        activity = get_object_or_404(Activity, pk=pk)
        # Update `activity` with partial data
        serializer = ActivitySerializer(activity, request.data, partial=True)

        if serializer.is_valid():
            # Get and save new objects if necessary
            if 'tag_IDs' in request.data:
                tag_IDs = request.data["tag_IDs"]
                serializer.save(tag_IDs=tag_IDs)
            if 'material_IDs' in request.data:
                material_IDs = request.data["material_IDs"]
                serializer.save(material_IDs=material_IDs)
            if 'resource_IDs' in request.data:
                resource_IDs = request.data["resource_IDs"]
                serializer.save(resource_IDs=resource_IDs)
            if 'activity_rels' in request.data:
                activity_rels = request.data["activity_rels"]
                serializer.save(activity_rels=activity_rels)
            if 'curriculum_rels' in request.data:
                curriculum_rels = request.data["curriculum_rels"]
                serializer.save(curriculum_rels=curriculum_rels)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurriculumViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer

    def create(self, request):
        # print "request data: "
        # print request.data

        serializer = CurriculumSerializer(data=request.data)

        if serializer.is_valid():
            # Look for optional activities passed in
            if "activity_rels" in request.data:
                activity_rels = request.data["activity_rels"]
                # Save new curriculum instance and pass in list of activities to be associated
                serializer.save(
                    activity_rels=activity_rels
                )
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print serializer.errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CurriculumActivityRelationshipViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = CurriculumActivityRelationship.objects.all()
    serializer_class = CurriculumActivityRelationshipSerializer
