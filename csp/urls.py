from munch import views
from django.conf.urls import patterns, include, url
from rest_framework.routers import SimpleRouter
from django.contrib import admin
admin.autodiscover()

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope


from munch.viewsets.user import UserViewSet

router = SimpleRouter(trailing_slash=True)
router.register(r'api/user', UserViewSet)

urlpatterns = patterns('',
					   url(r'', include(router.urls)),
					   url(r'^api/auth/login/$', views.Login.as_view()),
					   url(r'^api/auth/logout/$', views.Logout.as_view()),
					   url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
                       url(r'^api/oauth2-ng/token', views.Oauth2TokenView.as_view()),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
					   url(r'^admin/', include(admin.site.urls)),
                       )