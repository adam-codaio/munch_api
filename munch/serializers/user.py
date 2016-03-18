from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import ugettext_lazy as _
from munch import models
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from csp import settings
from munch.validators.utils import *
from rest_framework import status

class UserSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
	name = serializers.CharField(required=False)
	is_customer = serializers.BooleanField(required=False, write_only=True)
	is_restaurant = serializers.BooleanField(required=False, write_only=True)

	class Meta:
		model = models.User
		fields = ('id', 'email', 'name', 'is_customer', 'is_restaurant')

	def __init__(self, validate_non_fields=False, **kwargs):
		super(UserSerializer, self).__init__(**kwargs)
		self.validate_non_fields = validate_non_fields

	def create(self, **kwargs):
		user = User.objects.create_user(username=self.validated_data.get('email'), email=self.validated_data.get('email'),
										password=self.initial_data.get('password'))

		if self.validated_data.get('is_customer', False):
			customer = models.Customer()
			customer.user = user
			customer.name = self.initial_data.get('name')
			customer.save()
			id = customer.id

		if self.validated_data.get('is_restaurant', False):
			restaurant = models.Restaurant()
			restaurant.user = user
			restaurant.name = self.initial_data.get('name')
			restaurant.save()
			id = restaurant.id

		return id
