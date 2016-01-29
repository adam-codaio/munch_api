from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import ugettext_lazy as _
from munch import models
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from csp import settings
from munch.utils import Oauth2Utils
from munch.validators.utils import *
from rest_framework import status

class UserSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
	name = serializers.CharField(required=False)
	is_customer = serializers.BooleanField(required=False, write_only=True)
	is_restaurant = serializers.BooleanField(required=False, write_only=True)

	class Meta:
		model = models.User
		validators = [
			EqualityValidator(
				fields=['password1', 'password2']
			),
			LengthValidator('password1', 8),
		]
		fields = ('id', 'email', 'name', 'is_customer', 'is_restaurant')

	def __init__(self, validate_non_fields=False, **kwargs):
		super(UserSerializer, self).__init__(**kwargs)
		self.validate_non_fields = validate_non_fields

	# def validate_email(self, value):
	#     user = User.objects.filter(email=value)
	#     if user:
	#         raise ValidationError("That email is already in use.")
	#     return value

	def create(self, **kwargs):
		user = User.objects.create_user(username=self.validated_data.get('email'), email=self.validated_data.get('email'),
										password=self.initial_data.get('password1'))

		if self.validated_data.get('is_customer', True):
			customer = models.Customer()
			customer.user = user
			customer.name = self.initial_data.get('name')
			customer.save()

		if self.validated_data.get('is_restaurant', False):
			restaurant = models.Restaurant()
			restaurant.user = user
			restaurant.name = self.initial_data.get('name')
			restaurant.save()

		# email activation
		# if settings.EMAIL_ENABLED:
		#send email
		#active = false
		return user
