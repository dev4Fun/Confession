from django.db import models
from django.utils import timezone

# Create your models here.
class Confession(models.Model):

	CONFESSION_STATUS = (
		("S","Submitted"),
		("P","Posted"))

	title = models.CharField(max_length=50, default="Untitled")
	text = models.CharField(max_length=500)
	status = models.CharField(max_length=1,choices=CONFESSION_STATUS, default = "S")
	pub_date = models.DateTimeField('date published', default=timezone.now()) 
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)
	author = models.CharField(max_length=50, default="Anonimus")

	def __unicode__(self):
		return self.title

	def is_popular(self):
		return (self.likes > self.dislikes)

	is_popular.boolean = True
	 