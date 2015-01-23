from django.contrib import admin

from lessons.models import Curriculum, Tag, Lesson, Relationship

class RelationshipInline(admin.StackedInline):
    model = Relationship
    fk_name = 'from_lesson'

class LessonAdmin(admin.ModelAdmin):
	inlines = [RelationshipInline]

admin.site.register(Lesson, LessonAdmin)
admin.site.register(Curriculum)
admin.site.register(Tag)