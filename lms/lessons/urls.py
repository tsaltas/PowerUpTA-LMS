from django.conf.urls import patterns, url

from lessons import views

urlpatterns = patterns('',
	# ex: /lessons/
	url(r'^$', views.LessonsIndexView.as_view(), name='lessons'),
	# ex: /lessons/5/
	# note: pk stands for primary key
	url(r'^(?P<pk>\d+)/$', views.LessonDetailView.as_view(), name='lesson-detail'),
	# ex: /lessons/new/
	url(r'^new/$', views.add_lesson, name='add-lesson'),
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