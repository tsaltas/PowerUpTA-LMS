from django.contrib import admin

from lessons.models import Curriculum, Tag, Material, Resource, Activity, ActivityRelationship, CurriculumActivityRelationship


admin.site.register(CurriculumActivityRelationship)

class ActivityRelationshipInline(admin.TabularInline):
    model = ActivityRelationship
    fk_name = 'from_activity'

class CurriculumRelationshipInline(admin.TabularInline):
    model = CurriculumActivityRelationship

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
	inlines = [ActivityRelationshipInline, CurriculumRelationshipInline]
	list_display = ('name', 'category')

	fieldsets = (
        ("Required:", {
            'fields': ('name', 'description', 'tags')
        }),
        ('Optional:', {
            'classes': ('collapse',),
            'fields': (
            	'teaching_notes',
            	'category',
            	'video_url',
            	'materials',
            	'resources',
            	'image'
            )
        }),
    )

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

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
	fields = (('name', 'url'),)
	list_display = ('name', 'url',)
	list_editable = ('name', 'url',)
	list_display_links = None

@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
	inlines = [CurriculumRelationshipInline]
	exclude = ('activities',)
	list_display = ('name', 'tagline','lower_grade', 'upper_grade', 'length_hours')

@admin.register(ActivityRelationship)
class ActivityRelationshipAdmin(admin.ModelAdmin):
	fields = (('from_activity', 'to_activity'), 'rel_type')
	list_display = ('from_activity', 'to_activity', 'rel_type')
	list_editable = ('rel_type',)