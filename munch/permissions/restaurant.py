from rest_framework import permissions

class IsRestaurantOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj == request.user.restaurant:
            return True
        return False