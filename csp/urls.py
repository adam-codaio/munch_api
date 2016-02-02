from munch import views
from django.conf.urls import patterns, include, url
from rest_framework.routers import SimpleRouter
from django.contrib import admin
admin.autodiscover()
from munch.viewsets.user import UserViewSet

router = SimpleRouter(trailing_slash=True)
router.register(r'api/user', UserViewSet)

urlpatterns = patterns('',
					   url(r'', include(router.urls)),
					   url(r'^api/auth/$', views.Authenticate.as_view()),
					   url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
					   url(r'^admin/', include(admin.site.urls)),
                       )