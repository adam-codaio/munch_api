from munch import models
from rest_framework import serializers
from munch.serializers.dynamic import DynamicFieldsModelSerializer
# from geopy import Nominatim, distance

class RestaurantSerializer(DynamicFieldsModelSerializer):
	# distance = serializers.SerializerMethodField()
	
	class Meta:
		model = models.Restaurant
 		fields = ('id', 'user', 'name', 'phone_number', 'address', 'hours', 'deleted',
				  'created_timestamp', 'last_updated',)# 'distance')
	
	# def get_distance(self, obj):
	# 	address = obj.address
	# 	geolocator = Nominatim()
	# 	location = geolocator.geocode(address)
	# 	latitude = self.context['data']['latitude']
	# 	longitude = self.context['data']['longitude']
	# 	return round(distance.vincenty((location.latitude, location.longitude), 
	# 				(self.context['data']['latitude'], self.context['data']['longitude'])).miles, 1)

