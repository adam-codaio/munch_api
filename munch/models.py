from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=32)
	phone_number = models.CharField(max_length=20)
	#Maybe regulate format of these a bit more in the future
	address = models.CharField(max_length=128, blank=True)
	latitude = models.FloatField()
	longitude = models.FloatField()
	hours = models.CharField(max_length=256, blank=True)
	deleted = models.BooleanField(default=False)
	created_timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)

class Customer(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=32)
	deleted = models.BooleanField(default=False)
	created_timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)

class Promotion(models.Model):
	text = models.CharField(max_length=32)
	repetition = models.IntegerField()
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
	expiration = models.DateTimeField()
	#Unclear what will come of retail value in the future
	retail_value = models.FloatField(null=True, blank=True)
	deleted = models.BooleanField(default=False)
	created_timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)

class Claim(models.Model):
	customer = models.ForeignKey(Customer, related_name='claim_customer', on_delete=models.CASCADE)
	promotion = models.ForeignKey(Promotion, related_name='claim_promotion', on_delete=models.CASCADE)
	is_redeemed = models.BooleanField(default=False)
	deleted = models.BooleanField(default=False)
	#acts as claim_time
	created_timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		unique_together = ('customer', 'promotion',)





