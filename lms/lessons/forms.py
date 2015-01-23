from django import forms
from lessons.models import Lesson, Curriculum, Tag

# New lesson form
class LessonForm(forms.ModelForm):
	class Meta:
		model = Lesson
		fields = '__all__'

# New curriculum form
class CurriculumForm(forms.ModelForm):
	class Meta:
		model = Curriculum
		fields = '__all__'

# New tag form

class TagForm(forms.ModelForm):
	class Meta:
		model = Tag
		fields = '__all__'