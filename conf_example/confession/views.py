from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import View
from django.views.generic import TemplateView

from .forms import *
from django.views import generic

# Create your views here.

from confession.models import Confession
from django.utils import timezone

# rewrite as a class view
def index_view(request):
	confession_list = Confession.objects.filter(status='S').order_by('-pub_date') # most recent first
	paginator = Paginator(confession_list, 3) # confessions per page 

	page = request.GET.get('page')
	try:
		confession_list = paginator.page(page)
	except PageNotAnInteger:
		confession_list = paginator.page(1)
	except EmptyPage:
		confession_list = paginator.page(paginator.num_pages)

	return render(request, 'confession/base.html', {
		'confession_list' : confession_list
		})

class AboutView(TemplateView):
	template_name = 'confession/about.html'

class Message_view(TemplateView):
	form_class = MessageForm
	template_name = 'confession/message.html'

	def get(self,request):
		form = self.form_class()
		return render(request, self.template_name , { 'form' : form})
	def post(self,request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			send_mail(
				cd['subject'],
				cd['message'],
				cd.get('email', 'noreply@example.com'),
				['siteowner@example.com'],
				)
	
			return render(request, 'confession/message.html', {
				'form' : form
				})
		return render(request, self.template_name , { 'form' : form })

class SubmitView(TemplateView):
	form_class = SubmitForm
	template_name = 'confession/submit.html'
	
	def get(self,request):
		form = self.form_class()
		return render(request, self.template_name, { 'form' : form })
	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			confession = Confession(title=cd['title'], text=cd['text'])
			confession.save()
			return render(request, self.template_name, { 
				'form' : form ,
				'success' : 'OK'
				})
		return render(request, self.template_name, { 'form' : form })


