from django.conf.urls import patterns, url

from lessons import views

urlpatterns = patterns('',
	# ex: lessons/activities/
	url(r'^actvities$', views.ActivitiesIndexView.as_view(), name='activities'),
	# ex: /lessons/activities/5/
	# note: pk stands for primary key
	url(r'^activities/(?P<pk>\d+)/$', views.ActivityDetailView.as_view(), name='activity-detail'),
	# ex: /lessons/activities/new/
	url(r'^activities/new/$', views.add_activity, name='add-activity'),
	# ex: /lessons/curricula
	url(r'^curricula/$', views.CurriculaIndexView.as_view(), name='curricula'),
	# ex: /lessons/curricula/5/
	# note: pk stands for primary key
	url(r'^curricula/(?P<pk>\d+)/$', views.CurriculumDetailView.as_view(), name='curriculum-detail'),
	# ex: /lessons/curricula/new/
	url(r'^curricula/new/$', views.add_curriculum, name='add-curriculum'),
	# ex: /lessons/tags/new/
	url(r'^tags/new/$', views.add_tag, name='add-tag'),
)