from django import forms
from captcha.fields import ReCaptchaField

"""
All the forms 
"""

class SubmitForm(forms.Form):
	captcha = ReCaptchaField() 
	title = forms.CharField(min_length=4, max_length=50)
	text = forms.CharField(min_length=10, max_length=500)

class MessageForm(forms.Form):
	captcha = ReCaptchaField() 
	subject = forms.CharField(min_length=3, max_length=50)
	email = forms.EmailField()
	message = forms.CharField(min_length=10, max_length=500)