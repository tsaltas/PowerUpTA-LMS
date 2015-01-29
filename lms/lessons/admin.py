from django.contrib import admin

from lessons.models import Curriculum, Tag, Material, Resource, Activity, ActivityRelationship

class RelationshipInline(admin.StackedInline):
    model = ActivityRelationship
    fk_name = 'from_activity'

class ActivityAdmin(admin.ModelAdmin):
	inlines = [RelationshipInline]

admin.site.register(Activity, ActivityAdmin)
admin.site.register(Curriculum)
admin.site.register(Tag)
admin.site.register(Material)
admin.site.register(Resource)
admin.site.register(ActivityRelationship)