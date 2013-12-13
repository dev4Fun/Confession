from django.test import TestCase
from confession.models import Confession
from confession.forms import *
from django.core.urlresolvers import reverse

import os
os.environ['RECAPTCHA_TESTING'] = 'True'

def create_confession(title='Untitled',text='None'):
	return Confession.objects.create(title=title, text=text)

# Create your tests here.
class SubmitViewTest (TestCase):

	def test_submit_forms_with_valdi_entries(self):
		form_data = {
		'title':'something',
		'text' : 'this is long enought,eh?',
		'recaptcha_response_field': 'PASSED'}
		form = SubmitForm(data=form_data)
		self.assertEqual(form.is_valid(), True)

	def test_submit_forms_with_invalid_title_length(self):
		form_data = {
		'title':'',
		'text' : 'This is a valid entry',
		'recaptcha_response_field': 'PASSED'}
		form = SubmitForm(data=form_data)
		self.assertEqual(form.is_valid(), False)

	def test_submit_forms_with_invalid_text_length(self):
		form_data = {
		'title':'Valid title',
		'text' : '<10',
		'recaptcha_response_field': 'PASSED'}
		form = SubmitForm(data=form_data)
		self.assertEqual(form.is_valid(), False)

	def test_submit_forms_with_invalid_captcha(self):
		form_data = {
		'title':'something',
		'text' : 'this is long enought,eh?',
		'recaptcha_response_field': 'FAILED'}
		form = SubmitForm(data=form_data)
		self.assertEqual(form.is_valid(), False)

class ConfessionViewTest(TestCase):
	def test_index_view_with_no_confessions(self):
		response = self.client.get(reverse('confession:index'))
		self.assertEquals(response.status_code, 200)
		self.assertContains(response, 'No confessions are available')
		self.assertQuerysetEqual(response.context['confession_list'], [])

	def test_index_view_with_one_confession(self):
		confession = create_confession()
		response = self.client.get(reverse('confession:index'))
		self.assertQuerysetEqual(response.context['confession_list'],
			['<Confession: Untitled>']
			)
		
	# test view with submitted and published confession

