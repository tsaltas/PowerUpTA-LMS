from django.conf.urls import patterns, url
from lessons import views
from rest_framework.routers import DefaultRouter

# API URLs determined automatically by the rest framework router
# Include URLs for the browsable API
urlpatterns = [
	url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]