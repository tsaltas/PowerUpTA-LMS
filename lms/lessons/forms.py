from django.forms import ModelForm
from lessons.models import Lesson, Curriculum, Tag

# New lesson form
class LessonForm(ModelForm):
	class Meta:
		model = Lesson
		fields = '__all__'

# New curriculum form
class CurriculumForm(ModelForm):
	class Meta:
		model = Curriculum
		fields = '__all__'

# New tag form

class TagForm(ModelForm):
	class Meta:
		model = Tag
		fields = '__all__'