from django.contrib import admin

from lessons.models import Curriculum, Tag, Material, Resource, Activity, ActivityRelationship



class RelationshipInline(admin.StackedInline):
    model = ActivityRelationship
    fk_name = 'from_activity'

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
	inlines = [RelationshipInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	fields = (('name', 'category'), 'logo')
	list_display = ('name', 'category', 'tag_logo')

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
	fields = (('name', 'url'),)
	list_display = ('name', 'url',)
	list_editable = ('name', 'url',)
	list_display_links = None

admin.site.register(Curriculum)
admin.site.register(Resource)
admin.site.register(ActivityRelationship)