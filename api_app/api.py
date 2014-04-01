from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication
from tastypie.resources import ModelResource, Resource
from django.conf.urls import url
from tastypie import fields
from tastypie.utils import trailing_slash
from models import Request, Blockedip
from helpers.scrapingobject import ScrapingObject, dict2obj
from serializer import CustomJSONSerializer
from django.http import HttpResponse, HttpResponseNotFound
import yaml
import pytz
import logging
import pdb


class RequestResource(ModelResource):
	class Meta:
		queryset = Request.objects.all()
		resource_name = 'request'
		allowed_methods = ['post']
		authorization= Authorization()
		authentication = ApiKeyAuthentication()
		serializer = CustomJSONSerializer(formats=['json'])

	def hydrate(self, bundle):
		bundle.data['sourceusername'] = bundle.request.GET['username']

		return bundle

class BlockedipResource(ModelResource):
	class Meta:
		queryset = Blockedip.objects.all()
		resource_name = 'blockedip'
		allowed_methods = ['get']
		authorization= Authorization()
		authentication = ApiKeyAuthentication()

	def get_object_list(self, request):
		username = request.GET['username']
		if 'index' in request.GET:
			index = request.GET['index']
			return super(BlockedipResource, self).get_object_list(request).filter(sourceusername=username, id__gt=index)
		else:
			return super(BlockedipResource, self).get_object_list(request).filter(sourceusername=username)


class ScrapingResource(Resource):
	scraper = None
	index = fields.IntegerField(attribute="index")
	domain = None

	def base_urls(self):
		return [
	        url(r"^(?P<website_togo>\w+)%s$" % (trailing_slash()), self.wrap_view('dispatch_list'), name="api_dispatch_list"),
	        url(r"^(?P<website_togo>\w+)/schema%s$" % (trailing_slash()), self.wrap_view('get_schema'), name="api_get_schema"),
	        url(r"^(?P<website_togo>\w+)/set/(?P<pk_list>\w[\w/;-]*)/$", self.wrap_view('get_multiple'), name="api_get_multiple"),
	        url(r"^(?P<website_togo>\w+)/(?P<pk>\w[\w/-]*)%s$" % (trailing_slash()), self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
	    ]

	class Meta:
		resource_name = 'scraping'
		#authorization= Authorization()
		#authentication = ApiKeyAuthentication()

	def get_object_list(self, request):
		results = []
		methodName = None
		pathName = ""

		if 'method' in request.GET:
			methodName = request.GET['method']
			if 'path' in request.GET:
				pathName = request.GET['path']
			else:
				pathName = "top-10-video-game-developers"

		else:
			methodName = "front-lists"

		if self.domain == "picturegram":
			base_url = "http://www.picturegr.am"
		else:
			base_url = "http://www.listnerd.com"

		self.scraper = ScrapingObject(url_root=base_url, name=methodName, path=pathName)

		for each in self.scraper.data:
			results.append(dict2obj(each))

		return results


	def obj_get_list(self, bundle, **kwargs):
		self.domain = kwargs['website_togo']
		return self.get_object_list(bundle.request)

	def full_dehydrate(self, bundle, for_list=False):
		for each in self.scraper.fields:
			bundle.data[each] = getattr(bundle.obj, each)

		return bundle


class ScrapingResource_picturegram(Resource):
	scraper = None
	index = fields.IntegerField(attribute="index")


	class Meta:
		resource_name = 'picturegram'
		#authorization= Authorization()
		#authentication = ApiKeyAuthentication()

	def get_object_list(self, request):
		results = []
		methodName = None
		pathName = ""

		if 'method' in request.GET:
			methodName = request.GET['method']
			if 'path' in request.GET:
				pathName = request.GET['path']
			else:
				pathName = "top-10-video-game-developers"

		else:
			methodName = "front-lists"

		#has to get from the database here (name => path and action)
		
		#ScrapingObject(url_root="http://www.listnerd.com", path="", outdiv='front-lists')	
		self.scraper = ScrapingObject(name=methodName, path=pathName)

		for each in self.scraper.data:
			results.append(dict2obj(each))

		return results


	def obj_get_list(self, bundle, **kwargs):
		return self.get_object_list(bundle.request)

	def full_dehydrate(self, bundle, for_list=False):
		for each in self.scraper.fields:
			bundle.data[each] = getattr(bundle.obj, each)

		return bundle

