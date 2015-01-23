from django.conf.urls import patterns, url

from lessons import views

urlpatterns = patterns('',
	# ex: /lessons/
	url(r'^$', views.LessonsIndexView.as_view(), name='lessons'),
	# ex: /lessons/curricula
	url(r'^curricula/$', views.CurriculaIndexView.as_view(), name='curricula'),
	# ex: /lessons/5/
	# note: pk stands for primary key
	url(r'^(?P<pk>\d+)/$', views.LessonDetailView.as_view(), name='lesson-detail'),
	# ex: /lessons/curricula/5/
	# note: pk stands for primary key
	url(r'^curricula/(?P<pk>\d+)/$', views.CurriculumDetailView.as_view(), name='curriculum-detail'),
	# ex: /lessons/5/components
	#url(r'^(?P<pk>\d+)/components/$', views.ResultsView.as_view(), name='components'),
	# ex: /lessons/5/extensions
	#url(r'^(?P<pk>\d+)/extensions/$', views.ResultsView.as_view(), name='extensions'),
	# ex: /lessons/5/curricula
	#url(r'^(?P<pk>\d+)/curricula/$', views.ResultsView.as_view(), name='curricula'),
)