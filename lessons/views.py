import sys

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import RequestContext
from django.views.generic import ListView, DetailView

from lessons.models import Curriculum, Activity, Tag, Material, Resource, CurriculumActivityRelationship

from lessons.serializers import TagSerializer, MaterialSerializer, ActivitySerializer, ResourceSerializer, CurriculumSerializer, CurriculumActivityRelationshipSerializer

from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response

class TagViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    # Custom function to associate activities with tag
    def create(self, request):
        print "inside the creation function"
        print "data is"
        print request.data
        print "test logo file size (inside views.py): " + str(request.data["logo"].size)

        serializer = TagSerializer(data = request.data)

        if serializer.is_valid():
            print "serializer was valid!"
            # Save new tag instance and pass in list of activities to be associated with the tag
            serializer.save(activities = request.data['activities'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print "serializer not valid"
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
        serializer = MaterialSerializer(data = request.data)

        if serializer.is_valid():
            # Save new material instance and pass in list of activities to be associated with the material
            serializer.save(activities = request.data['activities'])
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
        serializer = ResourceSerializer(data = request.data)

        if serializer.is_valid():
            # Save new resource instance and pass in list of activities to be associated with the resource
            serializer.save(activities = request.data['activities'])
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
        serializer = ActivitySerializer(data = request.data)

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
                        rel_errors+=1
            
            if "activity_rels" in request.data:
                activities = request.data["activity_rels"]
                for rel in activities:
                    try:
                        Activity.objects.get(pk=rel["activityID"])
                        activity_rels.append(rel)
                    except ObjectDoesNotExist:
                        rel_errors+=1
            # Save new activity instance and pass in lists of objects to be associated with the activity
            serializer.save(
                tag_IDs = request.data["tag_IDs"]
                , curriculum_rels = curriculum_rels
                , material_IDs = material_IDs
                , resource_IDs = resource_IDs
                , activity_rels = activity_rels
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
                serializer.save(tag_IDs = tag_IDs)
            if 'material_IDs' in request.data:
                material_IDs = request.data["material_IDs"]
                serializer.save(material_IDs = material_IDs)
            if 'resource_IDs' in request.data:
                resource_IDs = request.data["resource_IDs"]
                serializer.save(resource_IDs = resource_IDs)
            if 'activity_rels' in request.data:
                activity_rels = request.data["activity_rels"]
                serializer.save(activity_rels = activity_rels)
            if 'curriculum_rels' in request.data:
                curriculum_rels = request.data["curriculum_rels"]
                serializer.save(curriculum_rels = curriculum_rels)
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

    # TODO: Validate data before saving objects?
    def create(self, request):
        print "request is: "
        print request
        print "data: "
        print request.data
        print "post: "
        print request.POST
        print "get: "
        print request.GET
        # first create the new curriculum
        curriculum = Curriculum.objects.create(
            name = request.data["name"],
            description = request.data["description"],
            upper_grade = request.data["upper_grade"],
            lower_grade = request.data["lower_grade"]
        )
        # Add optional fields if provided by user
        if "tagline" in request.data:
            curriculum.tagline = request.data["tagline"]
        
        # try to save curriculum
        try :
            curriculum.save()
        except:
            return Response("Error creating new curriculum: " + str(sys.exc_info()[0]),
                            status=status.HTTP_400_BAD_REQUEST)

        # if user specified an activity, then try to create any activity-curriculum relationships
        if "activities" in request.data:
            try:
                for relationship in request.data["activities"]:
                    activity = get_object_or_404(Activity, pk=relationship["activity"])
                    relationship = CurriculumActivityRelationship.objects.create(
                        curriculum = curriculum,
                        activity = activity,
                        number = relationship["number"]
                    )
                    relationship.save()
            except:
                return Response("Error adding curriculum-activity relationships: " + str(sys.exc_info()[0]),
                                status=status.HTTP_400_BAD_REQUEST)
        # on success, return Response object
        return Response()

class CurriculumActivityRelationshipViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = CurriculumActivityRelationship.objects.all()
    serializer_class = CurriculumActivityRelationshipSerializer

# old methods from original django model
"""
class ActivitiesIndexView(ListView):
	model = Activity
	template_name = 'activities/index.html'
	context_object_name = 'activities'

class ActivityDetailView(DetailView):
    model = Activity
    template_name = 'activities/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ActivityDetailView, self).get_context_data(**kwargs)
        # Get the current activity object
        activity = context['activity']
        # Add in a QuerySet of all the tags
        context['tags'] = activity.tags.all()
        # Add in a QuerySet of all the sub-activities
        subs = activity.relationships_to.filter(rel_type='SUB')
        context['subs'] = [rel.from_activity for rel in subs]
        # Add in a QuerySet of all the super-activities
        supers = activity.relationships_to.filter(rel_type='SUP')
        context['supers'] = [rel.from_activity for rel in supers]
        # context['components'] = [rel.to_activity for rel in activity.from_activities.filter(style=RelationshipType.EXTENSION)]
        # Add in a QuerySet of all the extensions
        extensions = activity.relationships_to.filter(rel_type='EXT')
        context['extensions'] = [rel.from_activity for rel in extensions]
        # Add in a QuerySet of all the curricula
        context['curricula'] = [relationship.curriculum for relationship in activity.curriculum_relationships.all()]
        return context

# Create a new lesson
def add_activity(request):
    # Get the context from the request
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = ActivityForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new lesson to the database.
            form.save(commit=True)

            # The user will be shown the list of lessons
            return HttpResponseRedirect(reverse('lessons:activities'))
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = ActivityForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('activities/add_activity.html', {'form': form}, context)

class CurriculaIndexView(ListView):
	model = Curriculum
	template_name = 'curricula/index.html'
	context_object_name = 'curricula'

class CurriculumDetailView(DetailView):
	model = Curriculum
	template_name = 'curricula/detail.html'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(CurriculumDetailView, self).get_context_data(**kwargs)
		# Get the current curriculum object
		curriculum = context['curriculum']
		# Add in a QuerySet of all the lessons
		context['activities'] = [rel.activity for rel in curriculum.activity_relationships.all()]
		# Add in a QuerySet of all the tags from associated lessons
		context['tags'] = set()
		for activity in context['activities']:
			context['tags'] = context['tags'] | set(activity.tags.all())
		return context

# Create a new curriculum
def add_curriculum(request):
	# Get the context from the request
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = CurriculumForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new lesson to the database.
            form.save(commit=True)

            # The user will be shown the list of curricula
            return HttpResponseRedirect(reverse('lessons:curricula'))
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CurriculumForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('curricula/add_curriculum.html', {'form': form}, context)


class TagsIndexView(ListView):
    model = Tag
    template_name = 'tags/index.html'
    context_object_name = 'tags'

# Create a new tag
def add_tag(request):
	# Get the context from the request
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = TagForm(request.POST, request.FILES)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new lesson to the database.
            form.save(commit=True)

            # The user will be shown the list of tags
            return HttpResponseRedirect(reverse('lessons:tags'))
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = TagForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('tags/add_tag.html', {'form': form}, context)
"""