from munch import models
from datetime import datetime
from rest_framework import serializers
from munch.serializers.dynamic import DynamicFieldsModelSerializer
from rest_framework.exceptions import ValidationError

class PromotionSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = models.Project
        fields = ('id', 'text', 'repetition', 'restaurant', 'expiration', 'retail_value', 'deleted',
        			'created_timestamp', 'last_updated',)
        read_only_fields = ('created_timestamp', 'last_updated', 'deleted',)

    def create(self, **kwargs):
    	promotion = models.Promotion.objects.create(deleted=False, restaurant=kwargs['restaurant'])
        return project

    def delete(self, instance):
        instance.deleted = True
        instance.save()
        return instance

