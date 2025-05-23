from rest_framework import permissions

class IsProjectOwnerOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        # Chỉ cho phép admin hoặc manager tạo project (POST)
        if view.action == 'create' or request.method == 'POST':
            return hasattr(request.user, 'role') and request.user.role in ['admin', 'manager']
        return True

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner') and obj.owner == request.user:
            return True
        if hasattr(obj, 'managers') and request.user in obj.managers.all():
            return True
        if hasattr(request.user, 'role') and request.user.role in ['admin', 'manager']:
            return True
        return False