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
                return Response(response_data, status.HTTP_200_OK)
            else:
                raise AuthenticationFailed(_('Account is not activated yet.'))
        else:
            raise AuthenticationFailed(_('Username or password is incorrect.'))


