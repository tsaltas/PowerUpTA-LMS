from django.forms import ModelForm
from lessons.models import Activity, Curriculum, Tag


# New lesson form
class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        exclude = ['relationships']


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
