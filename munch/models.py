from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class PhoneNumber(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
    				message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=17, validators=[phone_regex], blank=True)

class Restaurant(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=32)
	phone_number = models.ForeignKey(PhoneNumber)
	#Maybe regulate format of these a bit more in the future
	address = models.CharField(max_length=128)
	hours = models.CharField(max_length=256)
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
	restaurant = models.ForeignKey(Restaurant)
	expiration = models.DateTimeField()
	#Unclear what will come of retail value in the future
	retail_value = models.FloatField(null=True, blank=True)
	deleted = models.BooleanField(default=False)
	created_timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)

class Claim(models.Model):
	customer = models.ForeignKey(Customer, related_name='claim_customer')
	promotion = models.ForeignKey(Promotion, related_name='claim_promotion')
	is_redeemed = models.BooleanField(default=False)
	deleted = models.BooleanField(default=False)
	#acts as claim_time
	created_timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		unique_together = ('customer', 'promotion',)





