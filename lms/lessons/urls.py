from django.conf.urls import patterns, url, include
from lessons import views
from rest_framework.routers import DefaultRouter

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'/tags', views.TagViewSet)
router.register(r'/materials', views.MaterialViewSet)
router.register(r'/resources', views.ResourceViewSet)
router.register(r'/activities', views.ActivityViewSet)
router.register(r'/curricula', views.CurriculumViewSet)
#router.register(r'curr-act-relationships', views.CurriculumActivityViewSet)
#router.register(r'activity-relationships', views.ActivityRelationshipViewSet)

# API URLs determined automatically by the rest framework router
# Include URLs for the browsable API
urlpatterns = [
	url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]