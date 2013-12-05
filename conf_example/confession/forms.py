from django import forms
from captcha.fields import ReCaptchaField

"""
All the forms 
"""

class SubmitForm(forms.Form):
	captcha = ReCaptchaField() 
	title = forms.CharField(max_length=50)
	text = forms.CharField(max_length=500)

class MessageForm(forms.Form):
	subject = forms.CharField(max_length=50)
	email = forms.EmailField()
	message = forms.CharField(max_length=500)