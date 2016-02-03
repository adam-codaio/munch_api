from munch import models
from datetime import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from munch.serializers.dynamic import DynamicFieldsModelSerializer
from munch.serializers.customer import CustomerSerializer
from munch.serializers.promotion import PromotionSerializer

class ClaimSerializer(DynamicFieldsModelSerializer):
    customer = CustomerSerializer()
    promotion = PromotionSerializer()

    class Meta:
        model = models.Claim
        fields = ('id', 'customer', 'promotion', 'is_redeemed', 'deleted', 'created_timestamp', 'last_updated',)
        read_only_fields = ('created_timestamp', 'last_updated', 'deleted',)

    def create(self, **kwargs):
        claim = models.Claim.objects.create(customer=kwargs['customer'], promotion=kwargs['promotion'])
        return claim

    def delete(self, instance):
        instance.deleted = True
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.is_redeemed = validated_data.get('is_redeemed', instance.is_redeemed)
        instance.save()
        return instance
