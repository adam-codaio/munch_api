from munch import models
from datetime import datetime
from rest_framework import serializers
from munch.serializers.dynamic import DynamicFieldsModelSerializer
from rest_framework.exceptions import ValidationError

class PromotionSerializer(DynamicFieldsModelSerializer):
    remaining = serializers.SerializerMethodField()

    class Meta:
        model = models.Promotion
        fields = ('id', 'text', 'repetition', 'restaurant', 'expiration', 'retail_value', 'deleted',
        			'created_timestamp', 'last_updated', 'remaining',)
        read_only_fields = ('created_timestamp', 'last_updated', 'deleted', 'remaining',)

    def create(self, **kwargs):
    	promotion = models.Promotion.objects.create(deleted=False, restaurant=kwargs['restaurant'])
        return promotion

    def delete(self, instance):
        instance.deleted = True
        instance.save()
        return instance

    def get_remaining(self, obj):
        #TODO count remaining available
        return 0

