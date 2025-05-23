from rest_framework import permissions

class IsTaskOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Chỉ cho phép xem (GET, HEAD, OPTIONS) hoặc là chủ sở hữu task
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.userId == request.user