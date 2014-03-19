from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication
from tastypie.resources import ModelResource
from models import Request, Blockedip
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
		return super(BlockedipResource, self).get_object_list(request).filter(sourceusername=username)


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
