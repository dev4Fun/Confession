from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
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
	confession_list = Confession.objects.all()
	paginator = Paginator(confession_list, 2) # confessions per page 

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

class DetailView(generic.DetailView):
	model = Confession
	template_name = 'confession/detail.html'

	def get_queryset(self):
		""" 
		Excludes unpublished confessions
		"""
		return Confession.objects.filter(status='S')

class AboutView(TemplateView):
	template_name = 'confession/about.html'

def message_view(request):
	if request.method == 'POST':
		form = MessageForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			send_mail(
				cd['subject'],
				cd['message'],
				cd.get('email', 'noreply@example.com'),
				['siteowner@example.com'],
				)
			return render(request, 'confession/message.html')
		else:
			form = MessageForm()

	return render(request, 'confession/message.html')

class SubmitView(TemplateView):
	form_class = SubmitForm
	
	def get(self,request):
		form = self.form_class()
		return render(request, 'confession/submit.html', { 'form' : form })
	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			confession = Confession(title=cd['title'], text=cd['text'])
			confession.save()
			return HttpResponseRedirect('/success/')
		return render(request, 'confession/submit.html', { 'form' : form })

class SuccessView(TemplateView):
	def get(self,request):
		return render(request, 'confession/success.html', 
			{
				'message' : message
				}

				)

