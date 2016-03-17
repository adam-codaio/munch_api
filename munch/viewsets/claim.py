from rest_framework import status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from munch.models import Claim, Promotion
from munch.permissions.user import IsCustomer
from munch.permissions.claim import IsClaimOwner
from munch.serializers.claim import *
from munch.serializers.promotion import *
from datetime import datetime
from oauth2_provider.ext.rest_framework import OAuth2Authentication

class ClaimViewSet(viewsets.ModelViewSet):
	queryset = Claim.objects.filter(deleted=False)
	serializer_class = ClaimSerializer
	permission_classes = [IsCustomer, IsAuthenticated]

	def create(self, request, *args, **kwargs):
		promotion = Promotion.objects.get(pk=request.data['promotion_id'])
		claim_serializer = ClaimSerializer()
		claim = Claim.objects.filter(promotion=promotion, customer=request.user.customer)
		if len(claim) == 0:
			data = claim_serializer.create(promotion=promotion, customer=request.user.customer)
			response_data = {
				"id": data.id,
				"created": data.created_timestamp
			}
			return Response(data=response_data, status=status.HTTP_200_OK)
		else:
			return Response(data={"message": "You've already claimed that promotion!"},
						    status=status.HTTP_400_BAD_REQUEST)

	#should add permission classes here
	def update(self, request, *args, **kwargs):
		instance = self.get_object()
		claim_serializer = ClaimSerializer(instance=instance, data=request.data, partial=True)
		if claim_serializer.is_valid():
			claim_serializer.update(instance, claim_serializer.validated_data)
			return Response(data={"message": "Claim updated successfully!"}, status=status.HTTP_200_OK)
		else:
			return Response(data=claim_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	#maybe we should use this
	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		claim_serializer = ClaimSerializer(instance=instance)
		claim_serializer.delete(instance)
		return Response(data={"message": "Claim deleted successfully"}, status=status.HTTP_200_OK)

	#this needs to be fixed
	#handle permissions
	@list_route(methods=['get'], permission_classes=[IsAuthenticated, IsClaimOwner], url_path='list_claims')
	def list_claims(self, request, *args, **kwargs):
		claims = Claim.objects.filter(deleted=False)
		claim_serializer = ClaimSerializer(instance=claims, many=True, fields=('id', 'promotion', 'is_redeemed',))
		return Response(data=claim_serializer.data, status=status.HTTP_200_OK)

