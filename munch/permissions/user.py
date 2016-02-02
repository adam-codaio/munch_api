from rest_framework import permissions
from csp import settings

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'customer')


class IsRestaurant(permissions.BasePermission):
    def has_object_permission(self, request, view, object):
        return hasattr(request.user, 'restaurant')