from munch import models
from rest_framework import serializers
from munch.serializers.dynamic import DynamicFieldsModelSerializer
from geopy import Nominatim, distance

class RestaurantSerializer(DynamicFieldsModelSerializer):


	class Meta:
		model = models.Restaurant
 		fields = ('id', 'user', 'name', 'phone_number', 'address', 'hours', 'deleted',
				  'created_timestamp', 'last_updated', 'latitude', 'longitude',)


	def update(self, instance, validated_data):
		instance.name = validated_data.get('name', instance.name)
		instance.address = validated_data.get('address', instance.address)
		instance.hours = validated_data.get('hours', instance.hours)
		instance.phone_number = validated_data.get('phone_number', instance.phone_number)
		if validated_data.get('address', False):
			geolocator = Nominatim()
			location = geolocator.geocode(instance.address)
			instance.latitude = location.latitude
			instance.longitude = location.longitude
		instance.save()
		return instance
	
	def delete(self, instance):
		instance.deleted = True
		instance.save()
		return instance
	

