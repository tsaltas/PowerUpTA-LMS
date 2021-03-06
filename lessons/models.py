from django.db import models


class Tag(models.Model):
    """
    Tags are short strings used to label and categorize activities and curricula.
    Examples: "front-end", "recursion", "html", "30 minutes", "beginner"
    Tags are organized into categories
    """
    CATEGORIES = (
        # First element of tuple is the value stored in the DB
        # Second element of tuple is displayed by the default form widget or in a ModelChoiceField
        # Given an instance of a Tag object called "t", the display value can be accessed like this: t.get_category_display()
        ('Language', 'Language'),
        ('Technology', 'Technology'),
        ('Difficulty', 'Difficulty'),
        ('Length', 'Length'),
        ('Concept', 'Concept'),
        ('Misc', 'Miscellaneous'),
    )
    # REQUIRED
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=15, choices=CATEGORIES)
    # A tag has a many-to-many relationship with activities (DEFINED IN ACTIVITY)

    # OPTIONAL
    logo = models.ImageField(upload_to='tag_logos', blank=True, null=True, default='gray-box.jpg')

    def __unicode__(self):
        return self.name + " (" + self.category + ")"

    def tag_logo(self):
        return '<img src="{}" alt="{}" height="40" width="40">'.format(self.logo.url, self.name + " logo")
    tag_logo.allow_tags = True


class Material(models.Model):
    """
    Materials are documents required to complete an activity.
    """
    # ALL REQUIRED
    name = models.CharField(max_length=50, unique=True)
    url = models.URLField()
    # A material has a many-to-many relationship with activities (DEFINED IN ACTIVITY)

    def __unicode__(self):
        return self.name + ": " + self.url


class Resource(models.Model):
    """
    Resources are documents that may be useful to complete an activity or for further reading.
    """
    # ALL REQUIRED
    name = models.CharField(max_length=50, unique=True)
    url = models.URLField()
    # A material has a many-to-many relationship with activities (DEFINED IN ACTIVITY)

    def __unicode__(self):
        return self.name + ": " + self.url


class Activity(models.Model):
    """
    An activity is a single exercise for a student.
    """
    CATEGORIES = (
        # First element of tuple is the value stored in the DB
        # Second element of tuple is displayed by the default form widget or in a ModelChoiceField
        # Given an instance of an Activity object called "a", the display value can be accessed like this: a.get_category_display()
        ('Offline', 'Offline'),
        ('Online', 'Online'),
        ('Discussion', 'Discussion'),
        ('Extension', 'Extension'),
    )

    # REQUIRED
    name = models.CharField(max_length=50, unique=True)
    tags = models.ManyToManyField(Tag, related_name='activities')
    # OPTIONAL
    description = models.TextField(blank=True)
    category = models.CharField(max_length=15, choices=CATEGORIES, blank=True, null=True)
    teaching_notes = models.TextField(blank=True)
    video_url = models.URLField(blank=True)  # Assuming link to YouTube
    image = models.ImageField(upload_to='activity_images', blank=True)
    relationships = models.ManyToManyField('self',
        through='ActivityRelationship',
        symmetrical=False,
        blank=True
    )
    materials = models.ManyToManyField(Material, blank=True, related_name="activities")
    resources = models.ManyToManyField(Resource, blank=True, related_name="activities")
    # An activity has a many-to-many relationship with Curriculum (defined in curriculum)

    class Meta:
        verbose_name_plural = "activities"

    def __unicode__(self):
        if self.category:
            return self.get_category_display() + ": " + self.name
        else:
            return self.name

    def get_curricula(self):
        return [relationship.curriculum.id for relationship in self.curriculum_relationships.all()]

    def get_relationships(self):
        return [(relationship.from_activity.id, relationship.get_rel_type_display()) for relationship in self.relationships_to.all()]


class Step(models.Model):
    """
    An activity consists of steps (which have links to other activities).
    """
    # REQUIRED
    text = models.CharField(max_length=50)
    activity = models.ForeignKey(Activity, related_name='steps')
    number = models.IntegerField()
    # OPTIONAL
    step_activity = models.ForeignKey(Activity, blank=True, null=True)  # ID number of the activity which is the step

    def __unicode__(self):
        return self.text


class Curriculum(models.Model):
    """
    A curriculum is a set of activities on a specific theme. A class follows a curriculum.
    """
    GRADES = (
        # First element of tuple is the value stored in the DB
        # Second element of tuple is displayed by the default form widget or in a ModelChoiceField
        # Given an instance of a Curriculum object called "c", the display value can be accessed like this: c.get_grade_display()
        (0, 'K'),
        (1, 'First'),
        (2, 'Second'),
        (3, 'Third'),
        (4, 'Fourth'),
        (5, 'Fifth'),
        (6, 'Sixth'),
        (7, 'Seventh'),
        (8, 'Eighth'),
        (9, 'Ninth'),
        (10, 'Tenth'),
        (11, 'Eleventh'),
        (12, 'Twelfth'),
    )
    # REQUIRED
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    lower_grade = models.IntegerField(choices=GRADES)
    upper_grade = models.IntegerField(choices=GRADES)
    # OPTIONAL
    tagline = models.CharField(max_length=100, blank=True)
    activities = models.ManyToManyField(Activity, through="CurriculumActivityRelationship", blank=True, related_name='curricula')

    class Meta:
        verbose_name_plural = "curricula"

    def __unicode__(self):
        return self.name

    def get_activities(self):
        return [relationship.activity.id for relationship in self.activity_relationships.all()]


class ActivityRelationship(models.Model):
    """
    Activities can be related to each other (but need not be)
    1) One activity is a sub-activity of another
    2) One activity is a super-lesson of another (symmetrical to the one above)
    3) One activity is a short extension of another
    """
    RELATIONSHIP_TYPES = (
        ('SUB', 'sub-activity'),
        ('SUP', 'super-activity'),
        ('EXT', 'extension'),
    )
    # ALL REQUIRED
    rel_type = models.CharField(max_length=3, choices=RELATIONSHIP_TYPES, verbose_name="Relationship Type")
    from_activity = models.ForeignKey(Activity, related_name='relationships_from')
    to_activity = models.ForeignKey(Activity, related_name='relationships_to')

    class Meta:
        unique_together = ('from_activity', 'to_activity')
        verbose_name = "activity relationship"
        verbose_name_plural = "activity relationships"

    def __unicode__(self):
        return self.from_activity.name + " is a " + self.get_rel_type_display() + " of " + self.to_activity.name


class CurriculumActivityRelationship(models.Model):
    """
    Relationship to capture the ordering of activities within a curriculum.
    """
    # ALL REQUIRED
    curriculum = models.ForeignKey(Curriculum, related_name='activity_relationships')
    activity = models.ForeignKey(Activity, related_name='curriculum_relationships')
    number = models.IntegerField()

    class Meta:
        unique_together = (('curriculum', 'activity'), ('curriculum', 'number'),)
        ordering = ['curriculum', 'number']
        verbose_name = "curriculum relationship"
        verbose_name_plural = "curriculum relationships"

    def __unicode__(self):
        return "\"{}\" is activity number {} of \"{}\" curriculum.".format(
            self.activity.name,
            self.number,
            self.curriculum.name
        )
