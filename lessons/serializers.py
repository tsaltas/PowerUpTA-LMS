from django.forms import widgets
from rest_framework import serializers
from lessons.models import Tag, Resource, Material, Activity, Curriculum, ActivityRelationship, CurriculumActivityRelationship

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'logo', 'category')

    def to_representation(self, instance):
      ret = super(TagSerializer, self).to_representation(instance)
      ret['category'] = instance.get_category_display()
      return ret

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('name', 'url')

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('name', 'url')

class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    tags = TagSerializer(many = True)
    materials = MaterialSerializer(many = True)
    resources = ResourceSerializer(many = True)

    relationships = serializers.HyperlinkedRelatedField(
      many=True
      , view_name='lessons:activity-detail'
      , queryset=ActivityRelationship.objects.all()
    )

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
                  'get_curricula',
                  'relationships',
                  'materials',
                  'resources',
                 )
    
    def to_representation(self, instance):
        ret = super(ActivitySerializer, self).to_representation(instance)
        ret['category'] = instance.get_category_display()
        return ret    

class CurriculumActivityRelationshipSerializer(serializers.ModelSerializer):
  activity = ActivitySerializer()
  curriculum = serializers.PrimaryKeyRelatedField(queryset=Curriculum.objects.all())

  class Meta:
    model = CurriculumActivityRelationship
    fields = ('id', 'curriculum', 'activity', 'number')

class CurriculumSerializer(serializers.HyperlinkedModelSerializer):
    activities = CurriculumActivityRelationshipSerializer(source='activity_relationships', many=True)
    
    class Meta:
        model = Curriculum
        fields = ('id',
                  'name',
                  'description',
                  'lower_grade',
                  'upper_grade',
                  'activities',
                  'tagline',
                 )
    
    def to_representation(self, instance):
        ret = super(CurriculumSerializer, self).to_representation(instance)
        # Uncomment these to display grades as words ("sixth") instead of numbers ("6")
        #ret['lower_grade'] = instance.get_lower_grade_display()
        #ret['upper_grade'] = instance.get_upper_grade_display()

        # Make grade 0 display as K
        if instance.lower_grade == 0:
          ret['lower_grade'] = "K"
        if instance.upper_grade == 0:
          ret['upper_grade'] = "K"
        
        return ret 