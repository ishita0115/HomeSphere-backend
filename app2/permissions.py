# app1/permissions.py

from rest_framework.permissions import BasePermission
from app1.models import User  # Import your custom user model from app1

class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsSellerUser(BasePermission):
    """
    Allows access only to seller users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 2


# class IsTutor(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role == 2

# class IsUser(BasePermission):
#     def has_permission(self, request, view):
#         # Check if the user has the 'role' attribute set to 'tutor'
#         return request.user.is_authenticated and request.user.role == 3

#     def has_object_permission(self, request, view, obj):
#         # Allow tutors to modify their own objects
#         return obj.user == request.user