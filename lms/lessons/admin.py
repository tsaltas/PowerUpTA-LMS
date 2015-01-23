from django.contrib import admin

from lessons.models import Curriculum, Tag, Lesson, LessonRelationship

class RelationshipInline(admin.StackedInline):
    model = LessonRelationship
    fk_name = 'from_lesson'

class LessonAdmin(admin.ModelAdmin):
	inlines = [RelationshipInline]

admin.site.register(Lesson, LessonAdmin)
admin.site.register(Curriculum)
admin.site.register(Tag)