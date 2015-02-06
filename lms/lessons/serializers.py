from django.forms import widgets
from rest_framework import serializers
from lessons.models import Tag, Resource, Material, Activity, Curriculum, ActivityRelationship, CurriculumActivityRelationship

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'logo', 'category')

    def to_representation(self, instance):
      ret = super(TagSerializer, self).to_representation(instance)
      ret['category'] = instance.get_category_display()
      return ret

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('id', 'name', 'url')

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('id', 'name', 'url')

class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='lessons:tag-detail')
    relationships = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='lessons:activity-detail')
    materials = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='lessons:material-detail')
    resources = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='lessons:resource-detail')

    class Meta:
        model = Activity
        fields = ('id',
                  'name',
                  'description',
                  'tags',
                  'category',
                  'teaching_notes',
                  'video_url',
                  'image',
                  'relationships',
                  'materials',
                  'resources',
                 )
    
    def to_representation(self, instance):
        ret = super(ActivitySerializer, self).to_representation(instance)
        ret['category'] = instance.get_category_display()
        return ret    

class CurriculumSerializer(serializers.HyperlinkedModelSerializer):
    activities = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='lessons:activity-detail')
    
    class Meta:
        model = Curriculum
        fields = ('name',
                  'description',
                  'lower_grade',
                  'upper_grade',
                  'length_hours',
                  'activities',
                  'tagline',
                 )
    
    def to_representation(self, instance):
        ret = super(CurriculumSerializer, self).to_representation(instance)
        ret['lower_grade'] = instance.get_lower_grade_display()
        ret['upper_grade'] = instance.get_upper_grade_display()
        return ret 