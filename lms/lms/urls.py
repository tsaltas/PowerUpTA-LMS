from django.conf.urls import patterns, include, url
from django.contrib import admin

#FOR LOCAL FILE SERVING:
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic import TemplateView

class SimpleStaticView(TemplateView):
    def get_template_names(self):
        return [self.kwargs.get('template_name') + ".html"]

    def get(self, request, *args, **kwargs):
        from django.contrib.auth import authenticate, login
        if request.user.is_anonymous():
            # Auto-login the User for Demonstration Purposes
            user = authenticate()
            login(request, user)
        return super(SimpleStaticView, self).get(request, *args, **kwargs)
        
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api', include('lessons.urls', namespace='lessons')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^(?P<template_name>\w+)$', SimpleStaticView.as_view(), name='example'),
    url(r'^$', TemplateView.as_view(template_name='lessons/curriculum-list-basic.html')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
