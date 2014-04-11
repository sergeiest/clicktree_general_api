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
	time = models.DateTimeField(auto_now_add=True)

class Users(models.Model):
	name = models.CharField(max_length=255, blank=True)
	company = models.CharField(max_length=255, blank=True)
	authentication_id = models.IntegerField(blank=True, null=True)
	created_at = models.DateTimeField(blank=True, null=True)
	updated_at = models.DateTimeField(blank=True, null=True)
	apikey = models.CharField(max_length=255, blank=True)
	status = models.IntegerField(blank=True, null=True)
	class Meta:
		managed = False
		db_table = 'users'
		app_label = 'dev_users'

class Apicalls(models.Model):
	user_id = models.IntegerField(blank=True, null=True)
	website = models.CharField(max_length=255, blank=True)
	method = models.CharField(max_length=255, blank=True)
	path = models.CharField(max_length=255, blank=True)
	created_at = models.DateTimeField(blank=True, null=True)
	updated_at = models.DateTimeField(blank=True, null=True)
	class Meta:
		managed = False
		db_table = 'apicalls'
		app_label = 'dev_users'

models.signals.post_save.connect(create_api_key, sender=User)