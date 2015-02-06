from django.forms import widgets
from rest_framework import serializers
from lessons.models import Tag, Resource, Material, Activity, Curriculum, ActivityRelationship, CurriculumActivityRelationship

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'logo', 'get_category_display')

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('id', 'name', 'url')

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('id', 'name', 'url')

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id',
                  'name',
                  'description',
                  'tags',
                  'get_category_display',
                  'teaching_notes',
                  'video_url',
                  'image',
                  'relationships',
                  'materials',
                  'resources',
                 )

class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = ('name',
                  'description',
                  'get_lower_grade_display',
                  'get_upper_grade_display',
                  'length_hours',
                  'activities',
                  'tagline',
                 )

class ActivityRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityRelationship
        fields = ('get_rel_type_display',
                  'from_activity',
                  'to_activity',
                 )

class CurriculumActivityRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumActivityRelationship
        fields = ('curriculum',
                  'activity',
                  'number',
                 )