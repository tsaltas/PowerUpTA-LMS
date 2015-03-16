from django.forms import widgets
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from lessons.models import Tag, Resource, Material, Activity, Curriculum, ActivityRelationship, CurriculumActivityRelationship

class TagSerializer(serializers.ModelSerializer):
    activities = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ('id', 'name', 'logo', 'category', 'activities')

    def to_representation(self, instance):
      ret = super(TagSerializer, self).to_representation(instance)
      ret['category'] = instance.get_category_display()
      return ret

    # Custom function to associate activities with tags
    def create(self, validated_data):
    	# Get list of activities to be associated with the new tag
    	activities = validated_data.pop('activities')
    	 
    	tag = Tag.objects.create(**validated_data)

    	# Add activity-tag relationships
    	for activityID in activities:
    		tag.activities.add(get_object_or_404(Activity, pk=activityID))

    	tag.save()
    	return tag

class ResourceSerializer(serializers.ModelSerializer):
    activities = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Resource
        fields = ('id', 'name', 'url', 'activities')

    # Custom function to associate activities with resources
    def create(self, validated_data):
    	# Get list of activities to be associated with the new resource
    	activities = validated_data.pop('activities')
    	 
    	resource = Resource.objects.create(**validated_data)

    	# Add activity-resource relationships
    	for activityID in activities:
    		resource.activities.add(get_object_or_404(Activity, pk=activityID))

    	resource.save()
    	return resource

    def update(self, instance, validated_data):
    	# Update any fields passed in
    	instance.name = validated_data.get('name', instance.name)
    	instance.url = validated_data.get('url', instance.url)

    	# Add activity-resource relationships if specified
    	if 'activities' in validated_data:
    		# Remove any existing relationships
    		instance.activities.clear()
    		# Add new relationships
    		activities = validated_data.get('activities')
    		for activityID in activities:
    			instance.activities.add(get_object_or_404(Activity, pk=activityID))

    	instance.save()
    	return instance

class MaterialSerializer(serializers.ModelSerializer):
    activities = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Material
        fields = ('id', 'name', 'url', 'activities')

    # Custom function to associate activities with materials
    def create(self, validated_data):
    	# Get list of activities to be associated with the new material
    	activities = validated_data.pop('activities')
    	 
    	material = Material.objects.create(**validated_data)

    	# Add activity-material relationships
    	for activityID in activities:
    		material.activities.add(get_object_or_404(Activity, pk=activityID))

    	material.save()
    	return material

    def update(self, instance, validated_data):
    	# Update any fields passed in
    	instance.name = validated_data.get('name', instance.name)
    	instance.url = validated_data.get('url', instance.url)

    	# Add activity-material relationships if specified
    	if 'activities' in validated_data:
    		# Remove any existing relationships
    		instance.activities.clear()
    		# Add new relationships
    		activities = validated_data.get('activities')
    		for activityID in activities:
    			instance.activities.add(get_object_or_404(Activity, pk=activityID))

    	instance.save()
    	return instance

class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    tags = TagSerializer(many = True)
    materials = MaterialSerializer(many = True, required=False)
    resources = ResourceSerializer(many = True, required=False)

    relationships = serializers.HyperlinkedRelatedField(
      many=True
      , view_name='lessons:activity-detail'
      , queryset=ActivityRelationship.objects.all()
      , required=False
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