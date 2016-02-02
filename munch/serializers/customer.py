from munch import models
from rest_framework import serializers


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ('id', 'user', 'name', 'deleted', 'created_timestamp', 'last_updated',)