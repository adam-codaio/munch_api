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
		if serializer.is_valid():
			id = serializer.create()
			data = serializer.data
			data['id'] = id
			return Response(data=data, status=status.HTTP_200_OK)
		return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)