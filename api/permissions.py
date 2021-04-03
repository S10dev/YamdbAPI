from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.username == '':
            return False
        try:
            return request.user.groups.get_by_natural_key('moderator').is_moderator == True
        except Exception:
                return False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        if request.user.username == '':
            return False
        try:
            return request.user.groups.get_by_natural_key('admin').is_admin == True
        except Exception:
                return False


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, object):
        return obj.username == request.user


class IsSafe(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False
