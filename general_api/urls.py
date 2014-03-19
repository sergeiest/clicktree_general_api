from django.conf.urls import patterns, include, url
from tastypie.api import Api
from api_app.api import RequestResource, BlockedipResource

from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(RequestResource())

blocking_api = Api(api_name="block")
blocking_api.register(BlockedipResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'getLogs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v1_api.urls)),
    (r'^api/', include(blocking_api.urls))
)
