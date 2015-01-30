from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import RequestContext
from django.views.generic import ListView, DetailView

from lessons.forms import ActivityForm, TagForm, CurriculumForm
from lessons.models import Curriculum, Activity, Tag, ActivityRelationship

class ActivitiesIndexView(ListView):
	model = Activity
	template_name = 'activity/index.html'
	context_object_name = 'activities'

class ActivityDetailView(DetailView):
	model = Activity
	template_name = 'activities/detail.html'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(ActivityDetailView, self).get_context_data(**kwargs)
		# Get the current activity object
		activity = context['activity']
		# Add in a QuerySet of all the tags
		context['tags'] = activity.tags.all()
		# Add in a QuerySet of all the components
		context['components'] = [rel.to_activity for rel in activity.from_activities.filter(style=RelationshipType.EXTENSION)]
		# Add in a QuerySet of all the extensions
		context['extensions'] = [rel.from_lesson for rel in lesson.to_lessons.filter(style=RelationshipType.EXTENSION)]
		# Add in a QuerySet of all the curricula
		context['curricula'] = lesson.curricula.all()
		return context

# Create a new lesson
def add_activity(request):
    # Get the context from the request
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = LessonForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new lesson to the database.
            form.save(commit=True)
            print "we're returning the lessons page"

            # The user will be shown the list of lessons
            return HttpResponseRedirect('/lessons/')
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        print "it's not a post request"
        # If the request was not a POST, display the form to enter details.
        form = LessonForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('lessons/add_lesson.html', {'form': form}, context)

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
		context['lessons'] = curriculum.lessons.all()
		# Add in a QuerySet of all the tags from associated lessons
		context['tags'] = set()
		for lesson in curriculum.lessons.all():
			context['tags'] = context['tags'] | set(lesson.tags.all())
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
            return CurriculaIndexView.as_view()
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