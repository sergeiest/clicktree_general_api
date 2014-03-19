from django.db import models
from django.contrib.auth.models import User
from tastypie.models import create_api_key

from datetime import datetime
import pytz


class Request(models.Model):
	id = models.AutoField(primary_key=True)
	sourceusername = models.CharField(max_length=50,null=False,blank=False)
	userid = models.IntegerField(null=True,blank=True)
	host = models.CharField(max_length=200,null=False,blank=False)
	time = models.DateTimeField(default=datetime.now(pytz.utc))
	url = models.CharField(max_length=200,null=True,blank=True)
	method = models.CharField(max_length=4,null=True,blank=True)
	useragent = models.CharField(max_length=200,null=True,blank=True)
	encode = models.CharField(max_length=200,null=True,blank=True)
	referer = models.CharField(max_length=200,null=True,blank=True)
	lang = models.CharField(max_length=50,null=True,blank=True)
	ip = models.CharField(max_length=100,null=False,blank=False)
	port = models.CharField(max_length=5,null=True,blank=True)
	sessionid = models.CharField(max_length=100,null=True,blank=True)

class Blockedip(models.Model):
	id = models.AutoField(primary_key=True)
	active = models.IntegerField(default=1)
	sourceusername = models.CharField(max_length=50,null=False,blank=False)
	ip = models.CharField(max_length=100,null=False,blank=False)
	time = models.DateTimeField(default=datetime.now(pytz.utc))

models.signals.post_save.connect(create_api_key, sender=User)