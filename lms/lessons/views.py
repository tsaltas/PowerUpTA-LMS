from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from lessons.models import Curriculum, Lesson, Tag, Relationship

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
		context['components'] = Lesson.objects.filter(relationship__to_lessons=lesson)
		# Add in a QuerySet of all the extensions
		context['extensions'] = Lesson.objects.filter(relationship__from_lessons=lesson)
		# Add in a QuerySet of all the curricula
		context['curricula'] = lesson.curricula.all()
		return context

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