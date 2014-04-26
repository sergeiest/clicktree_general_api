from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.exceptions import Unauthorized
from django.contrib.auth.models import Group, User

class ScrapingAuthentication(Authentication):
	def is_authenticated(self, request, **kwargs):
		if not User.objects.filter(username=request.GET['username']).exists():
			return False

		user = User.objects.get(username = request.GET['username'])
		if user.groups.filter(name='apitool_users').exists():
			return True

		return False

	def get_identifier(self, request):
		return request.user.username


class ScrapingAuthorization(Authorization):
	def is_authorized(self, request, object=None):
		user = User.objects.get(username = request.GET['username'])
		if user.groups.filter(name='apitool_users').exists():
			return True

		return False

	def get_identifier(self, request):
		return request.user.username