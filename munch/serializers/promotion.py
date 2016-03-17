from munch import models
from datetime import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from munch.serializers.dynamic import DynamicFieldsModelSerializer
from munch.serializers.restaurant import RestaurantSerializer
from django.db import connection


class PromotionSerializer(DynamicFieldsModelSerializer):
    rating = serializers.SerializerMethodField()
    num_claims = serializers.IntegerField(read_only=True)
    restaurant = RestaurantSerializer(partial=True, read_only=True)

    class Meta:
        model = models.Promotion
        fields = ('id', 'text', 'repetition', 'restaurant', 'expiration', 'retail_value', 'deleted',
        			'created_timestamp', 'last_updated', 'rating', 'num_claims', 'deleted',)
        read_only_fields = ('created_timestamp', 'last_updated', 'deleted', 'rating', 'num_claims', 'deleted',)

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

    def get_rating(self, instance):
        customer_id = self.context['customer_id']
        query = '''
                SELECT COUNT(CASE WHEN is_redeemed='t' THEN 1 END) +
                       0.5 * COUNT(CASE WHEN is_redeemed='f' THEN 1 END) rating
                FROM munch_claim c
                INNER JOIN munch_promotion p ON c.promotion_id=p.id
                WHERE c.customer_id=%(customer)s AND p.restaurant_id=%(restaurant)s
                '''
        cursor = connection.cursor()
        cursor.execute(query, params={'customer': customer_id, 
                                               'restaurant': instance.restaurant.id})

        rating = cursor.fetchone()
        return float(rating[0]) * instance.retail_value

