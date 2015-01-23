from django.forms import ModelForm
from django.forms.models import modelformset_factory
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import RequestContext
from django.views.generic import ListView, DetailView

from lessons.forms import LessonForm, TagForm, CurriculumForm
from lessons.models import Curriculum, Lesson, Tag, LessonRelationship, RelationshipType

class LessonsIndexView(ListView):
	model = Lesson
	template_name = 'lessons/index.html'
	context_object_name = 'lessons'

class LessonDetailView(DetailView):
	model = Lesson
	template_name = 'lessons/detail.html'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(LessonDetailView, self).get_context_data(**kwargs)
		# Get the current lesson object
		lesson = context['lesson']
		# Add in a QuerySet of all the tags
		context['tags'] = lesson.tags.all()
		# Add in a QuerySet of all the components
		context['components'] = [rel.to_lesson for rel in lesson.from_lessons.filter(style=RelationshipType.EXTENSION)]
		# Add in a QuerySet of all the extensions
		context['extensions'] = [rel.from_lesson for rel in lesson.to_lessons.filter(style=RelationshipType.EXTENSION)]
		# Add in a QuerySet of all the curricula
		context['curricula'] = lesson.curricula.all()
		return context

# Create a new lesson
def add_lesson(request):
	# Get the context from the request
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = LessonForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new lesson to the database.
            form.save(commit=True)

            # The user will be shown the list of lessons
            return LessonsIndexView.as_view(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
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

# Create a new tag
def add_tag(request):
	# Get the context from the request
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = TagForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new lesson to the database.
            form.save(commit=True)

            # The user will be shown the list of lessons
            return LessonsIndexView.as_view()
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = TagForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('add_tag.html', {'form': form}, context)