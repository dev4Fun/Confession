from django.conf.urls import patterns, url

from confession import views
from confession.views import SubmitView, AboutView, SuccessView

urlpatterns = patterns('',
	url(r'^$', views.index_view, name='base'),
	url(r'^submit', SubmitView.as_view(), name='submit'),
	url(r'^about', AboutView.as_view(), name="about"),
	url(r'^message', views.message_view, name='message'),
	url(r'^success', SuccessView.as_view(), name='success'),
	url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
	)