from rest_framework import permissions
from csp import settings

class IsClaimOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.customer == request.user.customer:
            return True
        return False

class IsClaimIssuer(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if obj.promotion.restaurant == request.user.restaurant:
			return True
		return False