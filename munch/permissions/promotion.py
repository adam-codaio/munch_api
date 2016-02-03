from rest_framework import permissions
from csp import settings

class IsPromotionOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.restaurant == request.user.restaurant:
            return True
        return False