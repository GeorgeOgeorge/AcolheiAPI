from rest_framework import permissions


class UserLoginPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        else: return False
