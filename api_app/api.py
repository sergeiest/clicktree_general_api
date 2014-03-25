from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication
from tastypie.resources import ModelResource, Resource
from tastypie import fields
from models import Request, Blockedip
from helpers.scrapingobject import ScrapingObject
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
	index = fields.IntegerField(attribute="index")
	name = fields.CharField(attribute="name")
	meta = fields.CharField(attribute="meta")

	class Meta:
		resource_name = 'listnerd'
		#authorization= Authorization()
		#authentication = ApiKeyAuthentication()

	def get_object_list(self, request):
		results = []

		if 'method' in request.GET:
			methodName = request.GET['method']
		else:
			methodName = "some_default"

		#has to get from the database here (name => path and action)
		
		#ScrapingObject(url_root="http://www.listnerd.com", path="", outdiv='front-lists')	
		scraper = ScrapingObject()

		for each in scraper._data.items():
			results.append(dict2obj(each))

		return results

	def obj_get_list(self, bundle, **kwargs):
		return self.get_object_list(bundle.request)
		

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
