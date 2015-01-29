+from django.db import models

from django.conf import settings

class Curriculum(models.Model):
	"""
	A curriculum is a set of activities on a specific theme. A class follows a curriculum.
	"""
	GRADES = (
		# First element of tuple is the value stored in the DB
		# Second element of tuple is displayed by the default form widget or in a ModelChoiceField
		# Given an instance of a Curriculum object called "c", the display value can be accessed like this: c.get_grade_display()
		('0', 'K'),
		('1', 'First'),
		('2', 'Second'),
		('3', 'Third'),
		('4', 'Fourth'),
		('5', 'Fifth'),
		('6', 'Sixth'),
		('7', 'Seventh'),
		('8', 'Eighth'),
		('9', 'Ninth'),
		('10', 'Tenth'),
		('11', 'Eleventh'),
		('12', 'Twelfth'),
	)
	# REQUIRED
	name = models.CharField(max_length=50, unique=True)
	description = models.TextField()
	# A curriculum has a many-to-many relationship with lessons
	# Curriculum will inherit tags from the lessons
	lessons = models.ManyToManyField('Lesson', related_name="curricula")
	lower_grade = models.IntegerField(choices = GRADES)
	upper_grade = models.IntegerField(choices = GRADES)
	length_hours = models.IntegerField()
	# OPTIONAL
	tagline = models.CharField(max_length=100, blank=True)

	def __unicode__(self):
		return self.name + ": " + self.tagline

class Tag(models.Model):
	"""
	Tags are short strings used to label and categorize lessons and curricula.
	Examples: "front-end", "recursion", "html", "30 minutes", "beginner"
	Tags are organized into categories
	"""
	CATEGORIES = (
		# First element of tuple is the value stored in the DB
		# Second element of tuple is displayed by the default form widget or in a ModelChoiceField
		# Given an instance of a Tag object called "t", the display value can be accessed like this: t.get_category_display()
		('LAN', 'Language'),
		('TEC', 'Technology'),
		('DIF', 'Difficulty'),
		('LEN', 'Length'),
		('CON', 'Concept'),
	)
	# ALL REQUIRED
	name = models.CharField(max_length=50, unique=True)
	logo = models.ImageField(upload_to='tag_logos')
	category = models.CharField(choices=CATEGORIES)
	# A tag has a many-to-many relationship with lessons (DEFINED IN LESSON)
	
	def __unicode__(self):
		return self.category + ": " + self.name

class Lesson(models.Model):
	"""
	A lesson is a single exercise for a student.
	"""
	name = models.CharField(max_length=50, unique=True)
	description = models.TextField()
	
	# TODO: Add videos to lessons

	# A lesson has a recursive many-to-many relationship with itself
	# A lesson can be broken down in to components, and can have extensions, which are themselves lessons
	relationships = models.ManyToManyField('self',
		through='LessonRelationship',
		symmetrical=False)
	# A lesson has a many-to-many relationship with tags
	tags = models.ManyToManyField(Tag)
	# A lesson has a many-to-many relationship with curricula (defined ABOVE)

	def __unicode__(self):
		return self.name

	# TODO: Write methods that create symmetric relationships between lessons
	"""
	# Add a relationship with another lesson
	def add_relationship(self, lesson, style, symm=True):
		relationship, created = Relationship.objects.get_or_create(
			from_person = self,
			to_person = person,
			style = style
		)
		# Need to create the symmetric relationship on the other lesson
		# However this time we will pass in symm=False so it doesn't try to add a relationship back on self
		if symm:
			if style == COMPONENT:
				person.add_relationship(self, EXTENSION, False)
			else:
				person.add_relationship(self, COMPONENT, False)
		return relationship

	# Remove a relationship with another lesson
	def remove_relationship(self, lesson, style, symm=True):
		Relationship.objects.filter(
			from_person = self,
			to_person = person,
			style = style
		).delete()
		# Need to delete the symmetric relationship on the other lesson
		# However this time we will pass in symm=False so it doesn't try remove the relationship on self again
		if symm:
			if style == COMPONENT:
				person.remove_relationship(self, EXTENSION, False)
			else:
				person.remove_relationship(self, COMPONENT, False)

	# Get all the components / extension lessons
	def get_relationships(self, style):
		return self.relationships.filter(
			to_people__style = style,
			to_people__from_person=self
		)
	"""

class RelationshipType(models.Model):
	# Some information for the relationship model
	COMPONENT = 1
	EXTENSION = 2
	RELATIONSHIP_STYLES = (
		(COMPONENT, 'Component'),
		(EXTENSION, 'Extension'),
	)
	relationship_type = models.IntegerField(choices=RELATIONSHIP_STYLES)

	def __unicode__(self):
		# TODO: Fix this, kind of hackish right now
		return self.RELATIONSHIP_STYLES[self.relationship_type-1][1]

# Relationships to model many-to-many relationships that lessons have with each other
class LessonRelationship(models.Model):
	style = models.ManyToManyField(RelationshipType, blank=True, related_name='lesson_relationships')
	from_lesson = models.ForeignKey(Lesson, related_name='from_lessons')
	to_lesson = models.ForeignKey(Lesson, related_name='to_lessons')

	class Meta:
		unique_together = ('from_lesson', 'to_lesson')

	def __unicode__(self):
		# TODO: Make this print the type of relationship as well
		return "Relationship from " + self.from_lesson.name + " to " + self.to_lesson.name