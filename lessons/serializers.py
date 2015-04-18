from django.shortcuts import get_object_or_404

from rest_framework import serializers
from lessons.models import Tag, Resource, Material, Activity, Curriculum, ActivityRelationship, CurriculumActivityRelationship


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'logo', 'category')

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

    # Custom function to update activities list
    def update(self, instance, validated_data):
        # Update any fields passed in
        instance.name = validated_data.get('name', instance.name)
        instance.url = validated_data.get('url', instance.url)
        instance.url = validated_data.get('logo', instance.logo)

        # Add activity-tag relationships if specified
        if 'activities' in validated_data:
            # Remove any existing relationships
            instance.activities.clear()
            # Add new relationships
            activities = validated_data.get('activities')
            for activityID in activities:
                instance.activities.add(get_object_or_404(Activity, pk=activityID))

        instance.save()
        return instance


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

    # Custom function to update activities list
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

    # Custom function to update activities list
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
    tags = TagSerializer(many=True, required=False)
    materials = MaterialSerializer(many=True, required=False)
    resources = ResourceSerializer(many=True, required=False)

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
                  'get_relationships',
                  'materials',
                  'resources',
                 )

    def to_representation(self, instance):
        ret = super(ActivitySerializer, self).to_representation(instance)
        ret['category'] = instance.get_category_display()
        return ret

    # Custom function to associate objects with activities
    def create(self, validated_data):
        # Get lists of objects to be associated with the new activity
        tag_IDs = validated_data.pop('tag_IDs')
        resource_IDs = validated_data.pop('resource_IDs')
        material_IDs = validated_data.pop('material_IDs')
        curriculum_rels = validated_data.pop('curriculum_rels')
        activity_rels = validated_data.pop('activity_rels')

        activity = Activity.objects.create(**validated_data)

        # Add foreign key relationships
        for tagID in tag_IDs:
            activity.tags.add(get_object_or_404(Tag, pk=tagID))
        for resourceID in resource_IDs:
            activity.resources.add(get_object_or_404(Resource, pk=resourceID))
        for materialID in material_IDs:
            activity.materials.add(get_object_or_404(Material, pk=materialID))
        # save new activity
        activity.save()

        # create relationships that have through models
        create_activity_curriculum_relationships(activity, curriculum_rels)
        create_activity_activity_relationships(activity, activity_rels)

        return activity

    # Custom function to update objects associated with activity
    def update(self, instance, validated_data):
        # Update any fields passed in
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.teaching_notes = validated_data.get('teaching_notes', instance.teaching_notes)
        instance.video_url = validated_data.get('video_url', instance.video_url)
        instance.image = validated_data.get('image', instance.image)

        # Update any relationships if specified
        if 'tag_IDs' in validated_data:
            instance.tags.clear()
            tag_IDs = validated_data.get('tag_IDs')
            for tagID in tag_IDs:
                instance.tags.add(get_object_or_404(Tag, pk=tagID))
        if 'material_IDs' in validated_data:
            instance.materials.clear()
            material_IDs = validated_data.get('material_IDs')
            for materialID in material_IDs:
                instance.materials.add(get_object_or_404(Material, pk=materialID))
        if 'resource_IDs' in validated_data:
            instance.resources.clear()
            resource_IDs = validated_data.get('resource_IDs')
            for resourceID in resource_IDs:
                instance.resources.add(get_object_or_404(Resource, pk=resourceID))
        if 'activity_rels' in validated_data:
            instance.relationships_to.all().delete()
            create_activity_activity_relationships(instance, validated_data.get('activity_rels'))
        if 'curriculum_rels' in validated_data:
            instance.curriculum_relationships.all().delete()
            create_activity_curriculum_relationships(instance, validated_data.get('curriculum_rels'))

        instance.save()
        return instance


class CurriculumActivityRelationshipSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()
    curriculum = serializers.PrimaryKeyRelatedField(queryset=Curriculum.objects.all())

    class Meta:
        model = CurriculumActivityRelationship
        fields = ('id', 'activity', 'number')


class CurriculumSerializer(serializers.HyperlinkedModelSerializer):

    activities = ActivitySerializer(read_only=True, many=True)

    class Meta:
        model = Curriculum
        fields = ('id',
                  'name',
                  'description',
                  'lower_grade',
                  'upper_grade',
                  'tagline',
                  'activities'
                 )

    def to_representation(self, instance):
        ret = super(CurriculumSerializer, self).to_representation(instance)

        # Uncomment these to display grades as words ("sixth") instead of numbers ("6")
        # ret['lower_grade'] = instance.get_lower_grade_display()
        # ret['upper_grade'] = instance.get_upper_grade_display()

        # Make grade 0 display as K
        if instance.lower_grade == 0:
            ret['lower_grade'] = "K"
        if instance.upper_grade == 0:
            ret['upper_grade'] = "K"

        return ret


    # Custom function to associate activities with new curricula
    def create(self, validated_data):
        # Get lists of activities to be associated with the new curriculum
        if 'activity_rels' in validated_data:
            activity_rels = validated_data.pop('activity_rels')
        else:
            activity_rels = False

        curriculum = Curriculum.objects.create(**validated_data)

        if activity_rels:
            # Add curriculum-activity relationships
            create_curriculum_activity_relationships(curriculum, activity_rels)

        return curriculum

""" Helper Functions """


def create_activity_activity_relationships(activity, activity_rels):
    for rel in activity_rels:
        activity2 = get_object_or_404(Activity, pk=rel["activityID"])
        rel_type = rel["type"]

        relationship = ActivityRelationship(
            from_activity=activity2
            , to_activity=activity
            , rel_type=rel_type
        )
        relationship.save()

        # Need to make symmetrical relationship for sub / super activities
        if rel_type == "SUP":
            symmetric_relationship = ActivityRelationship(
                from_activity=activity
                , to_activity=activity2
                , rel_type="SUB"
            )
            symmetric_relationship.save()
        if rel_type == "SUB":
            symmetric_relationship = ActivityRelationship(
                from_activity=activity
                , to_activity=activity2
                , rel_type="SUP"
            )
            symmetric_relationship.save()


# TODO: Harmonize these two functions
def create_curriculum_activity_relationships(curriculum, activity_rels):
    for rel in activity_rels:
        activity = get_object_or_404(Activity, pk=rel["activityID"])
        relationship = CurriculumActivityRelationship.objects.create(
            curriculum=curriculum,
            activity=activity,
            number=rel["number"]
        )
        relationship.save()


# TODO: Harmonize these two functions
def create_activity_curriculum_relationships(activity, curriculum_rels):
    for rel in curriculum_rels:
        curr = get_object_or_404(Curriculum, pk=rel["curriculumID"])
        relationship = CurriculumActivityRelationship.objects.create(
            curriculum=curr
            , activity=activity
            , number=rel["number"]
        )
        relationship.save()
