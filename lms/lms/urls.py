from django.conf.urls import patterns, include, url
from django.contrib import admin

#FOR LOCAL FILE SERVING:
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('lessons.urls', namespace='lessons')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
