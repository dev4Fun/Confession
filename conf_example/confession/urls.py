from django.conf.urls import patterns, url

from confession import views

urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(), name='base'),
	url(r'^submit', views.submit_view, name='submit'),
	url(r'^about', views.about_view, name="about"),
	url(r'^message', views.message_view, name='message'),
	url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
	)