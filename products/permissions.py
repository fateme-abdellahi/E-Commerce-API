from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadonly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user and request.user.is_staff

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user and request.user.is_staff
    
class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
