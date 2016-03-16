from munch import models
from datetime import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from munch.serializers.dynamic import DynamicFieldsModelSerializer
from munch.serializers.restaurant import RestaurantSerializer


class PromotionSerializer(DynamicFieldsModelSerializer):
    remaining = serializers.SerializerMethodField()
    restaurant = RestaurantSerializer(partial=True, read_only=True)

    class Meta:
        model = models.Promotion
        fields = ('id', 'text', 'repetition', 'restaurant', 'expiration', 'retail_value', 'deleted',
        			'created_timestamp', 'last_updated', 'remaining',)
        read_only_fields = ('created_timestamp', 'last_updated', 'deleted', 'remaining',)

    def create(self, **kwargs):
        promotion = models.Promotion.objects.create(restaurant=kwargs['restaurant'], **self.validated_data)
        return promotion

    def delete(self, instance):
        instance.deleted = True
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.repetition = validated_data.get('repetition', instance.repetition)
        instance.expiration = validated_data.get('expiration', instance.expiration)
        instance.retail_value = validated_data.get('retail_value', instance.retail_value)
        instance.save()
        return instance

    def get_remaining(self, obj):
        #TODO count remaining available
        return 0
