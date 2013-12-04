from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

from django.views import generic
from django import forms

# Create your views here.

from confession.models import Confession
from django.utils import timezone

class IndexView(generic.ListView):
	template_name = 'confession/base.html'
	context_object_name = 'latest_confession_list'

	def get_queryset(self):
		""" Return the last ten published confessions """
		return Confession.objects.filter(
			pub_date__lte=timezone.now()
			).order_by('-pub_date') [:10]

class DetailView(generic.DetailView):
	model = Confession
	template_name = 'confession/detail.html'

	def get_queryset(self):
		""" 
		Excludes unpublished confessions
		"""
		return Confession.objects.filter(status='S')

def about_view(request):
	return render(request, 'confession/about.html')

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

def submit_view(request):
	if request.method == 'POST':
		form = SubmitForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			confession = Confession(title=cd['title'], text=cd['text'])
			confession.save()
			return HttpResponseRedirect('contacts/thanks/')
		else:
			form = SubmitForm()

	return render(request, 'confession/submit.html')

"""
All the forms 
"""
class SubmitForm(forms.Form):
	title = forms.CharField(max_length=50)
	text = forms.CharField(max_length=500)

class MessageForm(forms.Form):
	subject = forms.CharField(max_length=50)
	email = forms.EmailField()
	message = forms.CharField(max_length=500)