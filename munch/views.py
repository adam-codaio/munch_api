from django.shortcuts import render
from rest_framework import views as rest_framework_views
from rest_framework.views import APIView
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from munch.serializers.user import *
from munch.utils import *
from munch.models import *
from csp import settings
import stripe

class Authenticate(APIView):
    method_decorator(csrf_protect)

    def post(self, request, *args, **kwargs):
        from django.contrib.auth import authenticate as auth_authenticate

        email = request.data.get('email', '')
        password = request.data.get('password', '')
        user = auth_authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
            	response_data = dict()
                response_data["email"] = user.email
                response_data["client_id"] = settings.CLIENT_ID
                if hasattr(user, 'customer'):
                    response_data["id"] = user.customer.id
                elif hasattr(user, 'restaurant'):
                    response_data["id"] = user.restaurant.id
                return Response(response_data, status.HTTP_200_OK)
            else:
                raise AuthenticationFailed(_('Account is not activated yet.'))
        else:
            raise AuthenticationFailed(_('Username or password is incorrect.'))

class Payment(APIView):
    method_decorator(csrf_protect)

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        amount = request.data.get("amount")
        description = request.data.get("description")
        if request.user.customer.stripe_customer is None:
            token = request.data.get("stripeToken")
            try:
                stripe_customer = stripe.Customer.create(
                    source=token,
                    description="Customer" + str(request.user.customer.id) + ' ' + request.user.customer.name
                )
                customer = request.user.customer
                customer.stripe_customer = stripe_customer.id
                customer.save()
            except:
                return Response(data={"message": "Could not create customer"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                customer=request.user.customer.stripe_customer,
                description=description
            )
            return Response(data={"message": "Payment success"}, status=status.HTTP_200_OK)
        except stripe.error.CardError, e:
            return Response(data={"error":e}, status=status.HTTP_400_BAD_REQUEST)


