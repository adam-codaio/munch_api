from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import mixins
from django.shortcuts import get_object_or_404
from munch.models import *
from munch.serializers.user import UserSerializer

class UserViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
	"""
	    This class handles user view sets
	"""
	serializer_class = UserSerializer
	queryset = User.objects.all()
	lookup_value_regex = '[^/]+'
	lookup_field = 'email'

	def create(self, request, *args, **kwargs):
		serializer = UserSerializer(validate_non_fields=True, data=request.data, context={'request': request})
		print request.data
		if serializer.is_valid():
			serializer.create()
			return Response(serializer.data)
		return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)