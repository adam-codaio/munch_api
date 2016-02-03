from rest_framework import status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from munch.models import Promotion
from munch.permissions.user import IsRestaurant
from munch.permissions.promotion import IsPromotionOwner
from munch.serializers.promotion import *
from datetime import datetime
from oauth2_provider.ext.rest_framework import OAuth2Authentication

class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.filter(deleted=False)
    serializer_class = PromotionSerializer
    permission_classes = [IsRestaurant, IsPromotionOwner, IsAuthenticated]

    def create(self, request, *args, **kwargs):
        promotion_serializer = PromotionSerializer()
        data = promotion_serializer.create(restaurant=request.user.restaurant)
        return Response(status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        promotion_serializer = PromotionSerializer(instance=instance, data=request.data, partial=True)
        if promotion_serializer.is_valid():
            with transaction.atomic():
                promotion_serializer.update()
            return Response(data={"message": "Promotion updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(data=promotion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        promotion_serializer = PromotionSerializer(instance=instance)
        promotion_serializer.delete(instance)
        return Response(data={"message": "Promotion deleted successfully"}, status=status.HTTP_200_OK)

    @list_route(methods=['get'], permission_classes=[IsAuthenticated], url_path='list_promotions')
    def list_promotions(self, request, *args, **kwargs):
        #TODO filter more carefully
        #TODO TODO compute recommended values, etc
        promotions = Promotion.objects.filter(expiration__gt=datetime.now(), deleted=False)
        serializer = PromotionSerializer(instance=promotions, many=True, fields=('id', 'text', 'repetition', 'restaurant',
                                        'expiration', 'retail_value', 'remaining'), context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

