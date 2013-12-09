from django.conf.urls import patterns, url

from confession import views
from confession.views import SubmitView, AboutView, Message_view

urlpatterns = patterns('',
	url(r'^$', views.index_view, name='index'),
	url(r'^submit', SubmitView.as_view(), name='submit'),
	url(r'^about', AboutView.as_view(), name="about"),
	url(r'^message', Message_view.as_view(), name='message'),
	)