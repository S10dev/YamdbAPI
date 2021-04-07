from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.username == '':
            return False
        return request.user.role in ('admin', 'moderator')


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.username == '':
            return False
        return request.user.role == 'admin'

class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.username == '':
            return False


    def has_object_permission(self, request, view, object):
        return object == request.user


class IsSafe(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False


class IsPost(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        else:
            return False
