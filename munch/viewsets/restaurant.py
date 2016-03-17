from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from munch.models import Restaurant
from munch.permissions.restaurant import IsRestaurantOwner
from munch.serializers.restaurant import *
from datetime import datetime


class RestaurantViewSet(viewsets.ModelViewSet):
	queryset = Restaurant.objects.filter(deleted=False)
	serializer_class = RestaurantSerializer
	permission_classes = [IsRestaurantOwner, IsAuthenticated]

	def update(self, request, *args, **kwargs):
		instance = self.get_object()
		restaurant_serializer = RestaurantSerializer(instance=instance, data=request.data, partial=True)
		if restaurant_serializer.is_valid():
			restaurant_serializer.update(instance, restaurant_serializer.validated_data)
			return Response(data={"message": "Restaurant updated successfully!"}, status=status.HTTP_200_OK)
		else:
			return Response(data=restaurant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		restaurant_serializer = RestaurantSerializer(instance=instance)
		restaurant_serializer.delete(instance)
		return Response(data={"message": "Restaurant deleted successfully"}, status=status.HTTP_200_OK)
