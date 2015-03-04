import sys

from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import RequestContext
from django.views.generic import ListView, DetailView

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

class MaterialViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class ResourceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class CurriculumViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer

    # TODO: Validate data before saving objects?
    def create(self, request):
        # first create the new curriculum
        curriculum = Curriculum.objects.create(
            name = request.data["name"],
            tagline = request.data["tagline"],
            description = request.data["description"],
            upper_grade = request.data["upper_grade"],
            lower_grade = request.data["lower_grade"]
        )
        # try to save curriculum
        try :
            curriculum.save()
        except:
            return Response("Error creating curriculum: " + str(sys.exc_info()[0]),
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