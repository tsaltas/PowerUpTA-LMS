from django.contrib import admin

from lessons.models import Curriculum, Tag, Material, Resource, Activity, Step, ActivityRelationship, CurriculumActivityRelationship


class ActivityRelationshipInline(admin.TabularInline):
    model = ActivityRelationship
    fk_name = 'from_activity'


class CurriculumRelationshipInline(admin.TabularInline):
    model = CurriculumActivityRelationship


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    inlines = [ActivityRelationshipInline, CurriculumRelationshipInline]
    list_display = ('name', 'category')
    list_filter = ('category',)

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


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    inlines = [CurriculumRelationshipInline]
    exclude = ('activities',)
    list_display = ('name', 'tagline', 'lower_grade', 'upper_grade')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = (('name', 'category'), 'logo')
    list_display = ('name', 'category', 'tag_logo')
    list_filter = ('category',)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    fields = (('name', 'url'),)
    list_display = ('name', 'url',)
    list_editable = ('name', 'url',)
    list_display_links = None


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    fields = (('text', 'step_activity'),())
    list_display = ('name', 'url',)
    list_editable = ('name', 'url',)
    list_display_links = None


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    fields = (('text', 'activity', 'number'), 'step_activity')
    list_display = ('text', 'activity', 'number')
    list_filter = ('activity',)


@admin.register(ActivityRelationship)
class ActivityRelationshipAdmin(admin.ModelAdmin):
    fields = (('from_activity', 'to_activity'), 'rel_type')
    list_display = ('from_activity', 'to_activity', 'rel_type')
    list_editable = ('rel_type',)


@admin.register(CurriculumActivityRelationship)
class CurriculumRelationshipAdmin(admin.ModelAdmin):
    list_display = ('curriculum', 'activity', 'number')
    list_editable = ('curriculum', 'activity', 'number')
    list_filter = ('curriculum',)
    list_display_links = None
