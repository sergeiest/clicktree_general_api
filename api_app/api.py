from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication
from tastypie.resources import ModelResource, Resource
from tastypie import fields
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
	#name = fields.CharField(attribute="name")
	#meta = fields.CharField(attribute="meta")
	#item = fields.IntegerField(attribute="item")
	#position = fields.IntegerField(attribute="position")
	#title = fields.CharField(attribute="title")
	#vote = fields.CharField(attribute="vote")

	#attributes = ['index', 'name', 'meta', 'item', 'position', 'title', 'vote']

	class Meta:
		resource_name = 'listnerd'
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
				pathName = "list/top-10-video-game-developers"

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

	#def dehydrate(self, bundle):
	#	for each in attributes:
	#		if not each in bundle.data:
	#			bundle.data[each] = ""		

	#def dehydrate(self, bundle):
	#	bundle.data['user'] = bundle.request.META.

#for picturegram (for authentication from his server will be needed)
# class RequestResource(ModelResource):
#     class Meta:
#         queryset = Request.objects.all()
#         resource_name = 'request'
#         allowed_methods = ['get','post']
#         authorization= Authorization()
#         serializer = CustomJSONSerializer(formats=['json'])

#     def dispatch(self, request_type, request,  **kwargs):
#         if request.method == 'POST':
#             response = super(ModelResource, self).dispatch(request_type, request, **kwargs)
#         if request.method == 'GET':
#             if 'hub[challenge]' in request.GET:
#                 response = HttpResponse()
#                 content = request.GET['hub[challenge]']
#                 response.write(content)
#             else:
#                 response = HttpResponseNotFound()

#         return response
