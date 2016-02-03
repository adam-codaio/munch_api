from munch import models
from rest_framework import serializers
from munch.serializers.dynamic import DynamicFieldsModelSerializer


class PhoneNumberSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.PhoneNumber
		fields = ('id', 'phone_number',)

class RestaurantSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = models.Restaurant
        fields = ('id', 'user', 'name', 'phone_number', 'address', 'hours', 'deleted',
        		  'created_timestamp', 'last_updated',)