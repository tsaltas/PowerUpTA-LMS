from django.shortcuts import render
from django.views import generic

from lessons.models import Curriculum, Lesson, Tag, Relationship

class LessonsIndexView(generic.ListView):
	template_name = 'lessons/index.html'
	context_object_name = 'lessons'

	def get_queryset(self):
		"""
		Return all existing lessons
		"""
		return Lesson.objects.all()

class CurriculaIndexView(generic.ListView):
	template_name = 'curricula/index.html'
	context_object_name = 'curricula'

	def get_queryset(self):
		"""
		Return all existing curricula
		"""
		return Curriculum.objects.all()

class LessonDetailView(generic.DetailView):
	model = Lesson
	template_name = 'lessons/detail.html'

	def get_queryset(self):
		"""
		Return all lesson components
		"""
		return Lesson.objects.all()

class CurriculumDetailView(generic.DetailView):
	model = Lesson
	template_name = 'curricula/detail.html'

	def get_queryset(self):
		"""
		Return all Lessons associated with the curriculum
		"""
		return Lesson.objects.filter(curricula__contains=self)