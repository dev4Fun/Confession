from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.views import generic

from .forms import *


# Create your views here.

from confession.models import Confession
from django.utils import timezone

# rewrite as a class view
def index_view(request):
	sl = ":5" # default slicing for pagination
	confession_list = Confession.objects.filter(status='S').order_by('-pub_date') # most recent first
	paginator = Paginator(confession_list, 5) # confessions per page 
	# request.build_absolute_uri(reverse('confession:detail', args=[str(confession.id)])

	page = request.GET.get('page')
	if request.GET.get('page'):
		if int(page) == 2: # second page
			sl = ":5"
		if int(page) == (paginator.num_pages-1):
			sl = "-5:"
		elif int(page) == paginator.num_pages:
			sl = "-5:"
		elif int(page) > 2:
			sl = "%d:%d" % (int(page)-3,int(page)+2)

	try:
		confession_list = paginator.page(page)
	except PageNotAnInteger:
		confession_list = paginator.page(1)
	except EmptyPage:
		confession_list = paginator.page(paginator.num_pages)

	return render(request, 'confession/base.html', {
		'confession_list' : confession_list,
		'sl' : sl
		})

class DetailView(generic.DetailView):
	model = Confession

class AboutView(TemplateView):
	template_name = 'confession/about.html'

class MessageView(TemplateView):
	form_class = MessageForm
	template_name = 'confession/message.html'

	def get(self,request):
		form = self.form_class()
		return render(request, self.template_name , { 'form' : form})
	def post(self,request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			request.session['message-submitted'] = True
			cd = form.cleaned_data
			send_mail(
				cd['subject'],
				cd['message'],
				cd.get('email', 'noreply@example.com'),
				['siteowner@example.com'],
				)
	
			return HttpResponseRedirect(reverse('confession:success'))
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
			request.session['confession-submitted'] = True
			cd = form.cleaned_data
			confession = Confession(title=cd['title'], text=cd['text'])
			confession.save()
			return HttpResponseRedirect(reverse('confession:success'))
		return render(request, self.template_name, { 'form' : form })

class SuccessView(View):
	def get(self,request):
		if request.session.get('confession-submitted', False): # conf submission
			request.session.flush()
			return render(request, 'confession/success.html', {
				'message' : 'confession',
				'confession' : 'true'
				})
	
		if request.session.get('message-submitted', False): # message submission
			request.session.flush()
			return render (request, 'confession/success.html', {
				'message' : 'message',
				'e-mail' : 'true'
				})

		else: 
				return HttpResponseRedirect(reverse('confession:submit'))
			
